import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { TaskWebSocket } from '@/utils/websocket'
import type { Message, CoderMessage, WriterMessage, UserMessage, ModelerMessage, CoordinatorMessage, InterpreterMessage } from '@/utils/response'
// import messageData from '@/test/20250524-115938-d4c84576.json'
import { AgentType } from '@/utils/enum'
import { getTaskMessages } from '@/apis/commonApi'

export const useTaskStore = defineStore('task', () => {
  // 初始化时直接加载测试数据，确保页面首次渲染时有数据
  // const messages = ref<Message[]>(messageData as Message[])
  const messagesByTask = ref<Record<string, Message[]>>({})
  const currentTaskId = ref<string | null>(null)
  const messages = computed<Message[]>(() => {
    if (!currentTaskId.value) {
      return []
    }
    return messagesByTask.value[currentTaskId.value] ?? []
  })
  const seenMessageIdsByTask = new Map<string, Set<string>>()
  let ws: TaskWebSocket | null = null

  function getMessageTimestamp(message: Message): number | null {
    if (!message.created_at) {
      return null
    }
    const timestamp = Date.parse(message.created_at)
    return Number.isNaN(timestamp) ? null : timestamp
  }

  function sortMessages(items: Message[]) {
    return [...items].sort((left, right) => {
      const leftTs = getMessageTimestamp(left)
      const rightTs = getMessageTimestamp(right)
      if (leftTs == null || rightTs == null || leftTs === rightTs) {
        return 0
      }
      return leftTs - rightTs
    })
  }

  function isMessagePayload(payload: unknown): payload is Message {
    if (!payload || typeof payload !== 'object') {
      return false
    }
    const msgType = Reflect.get(payload, 'msg_type')
    return (
      typeof Reflect.get(payload, 'id') === 'string' &&
      typeof msgType === 'string' &&
      ['system', 'agent', 'user', 'tool'].includes(msgType)
    )
  }

  function setCurrentTask(taskId: string) {
    currentTaskId.value = taskId
    if (typeof window !== 'undefined') {
      window.localStorage.setItem('currentTaskId', taskId)
    }
  }

  function ensureTaskBucket(taskId: string) {
    if (!messagesByTask.value[taskId]) {
      messagesByTask.value[taskId] = []
    }
    if (!seenMessageIdsByTask.has(taskId)) {
      seenMessageIdsByTask.set(taskId, new Set())
    }
  }

  function appendMessage(taskId: string, message: Message) {
    ensureTaskBucket(taskId)
    const seenIds = seenMessageIdsByTask.get(taskId)
    if (message.id && seenIds?.has(message.id)) {
      messagesByTask.value[taskId] = sortMessages(
        messagesByTask.value[taskId].map((existing) =>
          existing.id === message.id ? message : existing,
        ),
      )
      return
    }
    if (message.id) {
      seenIds?.add(message.id)
    }
    messagesByTask.value[taskId] = sortMessages([
      ...messagesByTask.value[taskId],
      message,
    ])
  }

  function mergeMessages(taskId: string, incomingMessages: Message[]) {
    ensureTaskBucket(taskId)
    const existingMessages = messagesByTask.value[taskId]
    const mergedById = new Map<string, Message>()

    for (const message of [...existingMessages, ...incomingMessages]) {
      if (!message.id) {
        continue
      }
      mergedById.set(message.id, message)
    }

    const mergedMessages = Array.from(mergedById.values())
    messagesByTask.value[taskId] = sortMessages(mergedMessages)
    seenMessageIdsByTask.set(
      taskId,
      new Set(mergedMessages.map((message) => message.id)),
    )
  }

  // 连接 WebSocket
  function connectWebSocket(taskId: string) {
    if (ws) {
      ws.close()
      ws = null
    }
    setCurrentTask(taskId)
    ensureTaskBucket(taskId)

    const baseUrl = import.meta.env.VITE_WS_URL
    const wsUrl = `${baseUrl}/task/${taskId}`

    ws = new TaskWebSocket(wsUrl, (data) => {
      if (!isMessagePayload(data)) {
        console.warn('忽略非标准任务消息:', data)
        return
      }
      appendMessage(taskId, data)
    })
    // 初始化测试数据（已在上面初始化，这里可以注释掉）
    // messages.value = messageData as Message[]
    ws.connect()
  }

  async function loadTaskMessages(taskId: string) {
    setCurrentTask(taskId)
    ensureTaskBucket(taskId)
    try {
      const response = await getTaskMessages(taskId)
      const validMessages = (response.data ?? []).filter(isMessagePayload)
      mergeMessages(taskId, validMessages)
    } catch (error) {
      console.error('加载任务历史消息失败:', error)
    }
  }

  // 关闭 WebSocket
  function closeWebSocket() {
    ws?.close()
    ws = null
  }

  function addUserMessage(content: string) {
    const taskId = currentTaskId.value ?? 'local'
    appendMessage(taskId, {
      id: Date.now().toString(),
      msg_type: 'user',
      content: content,
    } as UserMessage)
  }

  // 下载消息
  function downloadMessages() {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(messages.value, null, 2))
    const downloadAnchorNode = document.createElement('a')
    downloadAnchorNode.setAttribute("href", dataStr)
    downloadAnchorNode.setAttribute("download", `${currentTaskId.value ?? 'task'}-messages.json`)
    document.body.appendChild(downloadAnchorNode)
    downloadAnchorNode.click()
    downloadAnchorNode.remove()
  }

  // 计算属性
  const chatMessages = computed(() =>
    messages.value.filter(
      (msg) => {
        if (msg.msg_type === 'agent' && msg.agent_type === AgentType.CODER && msg.content != null && msg.content != '') {
          return true
        }
        if (msg.msg_type === 'user') {
          return true
        }
        if(msg.msg_type === 'system') {
          return true
        }
        // if (msg.msg_type === 'tool' && msg.tool_name === 'execute_code') {
          // return true
        // }
        return false
      }
    )
  )

  const coordinatorMessages = computed(() =>
    messages.value.filter(
      (msg): msg is CoordinatorMessage =>
        msg.msg_type === 'agent' &&
        msg.agent_type === AgentType.COORDINATOR &&
        msg.content != null
    )
  )

  const modelerMessages = computed(() =>
    messages.value.filter(
      (msg): msg is ModelerMessage =>
        msg.msg_type === 'agent' &&
        msg.agent_type === AgentType.MODELER &&
        msg.content != null
    )
  )

  const coderMessages = computed(() =>
    messages.value.filter(
      (msg): msg is CoderMessage =>
        msg.msg_type === 'agent' &&
        msg.agent_type === AgentType.CODER &&
        msg.content != null
    )
  )

  const writerMessages = computed(() =>
    messages.value.filter(
      (msg): msg is WriterMessage =>
        msg.msg_type === 'agent' &&
        msg.agent_type === AgentType.WRITER &&
        msg.content != null
    )
  )

  // 添加代码执行工具消息的计算属性
  const interpreterMessage = computed(() =>
    messages.value.filter(
      (msg): msg is InterpreterMessage =>
        msg.msg_type === 'tool' &&
        'tool_name' in msg &&
        msg.tool_name === 'execute_code'
    )
  )

  const files = computed(() => {
    // 反向遍历消息找到最新的文件列表
    for (let i = coderMessages.value.length - 1; i >= 0; i--) {
      const msg = coderMessages.value[i]
      if ('files' in msg && msg.files && Array.isArray(msg.files) && msg.files.length > 0) {
        console.log('找到文件列表:', msg.files)
        return msg.files
      }
    }
    // 如果没有找到文件列表，返回空数组
    console.log('没有找到文件列表，返回空数组')
    return []
  })
  
  // 初始化连接
  // 如果需要自动连接，可以在这里添加代码
  // 例如：connectWebSocket('default')

  return {
    messages,
    chatMessages,
    coordinatorMessages,
    modelerMessages,
    coderMessages,
    writerMessages,
    interpreterMessage,
    files,
    loadTaskMessages,
    connectWebSocket,
    closeWebSocket,
    downloadMessages,
    addUserMessage
  }
}) 
