<script setup lang="ts">
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from '@/components/ui/resizable'
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs'
import CoderEditor from '@/components/AgentEditor/CoderEditor.vue'
import WriterEditor from '@/components/AgentEditor/WriterEditor.vue'
import ModelerEditor from '@/components/AgentEditor/ModelerEditor.vue'
import ChatArea from '@/components/ChatArea.vue'
import { onMounted, onBeforeUnmount, ref } from 'vue'
import { useTaskStore } from '@/stores/task'
import { getWriterSeque } from '@/apis/commonApi';
import { Button } from '@/components/ui/button';
import FilesSheet from '@/pages/task/components/FileSheet.vue'


const props = defineProps<{ task_id: string }>()
const taskStore = useTaskStore()

const writerSequence = ref<string[]>([]);

// 项目运行时长相关
const startTime = ref<number>(Date.now())
const currentTime = ref<number>(Date.now())
let timer: ReturnType<typeof setInterval> | null = null

// 格式化运行时长
const formatDuration = (ms: number): string => {
  const seconds = Math.floor(ms / 1000)
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const remainingSeconds = seconds % 60

  if (hours > 0) {
    return `${hours}h ${minutes}m ${remainingSeconds}s`
  } else if (minutes > 0) {
    return `${minutes}m ${remainingSeconds}s`
  } else {
    return `${remainingSeconds}s`
  }
}

// 计算运行时长
const runningDuration = ref<string>('0s')
const updateDuration = () => {
  currentTime.value = Date.now()
  runningDuration.value = formatDuration(currentTime.value - startTime.value)
}

console.log('Task ID:', props.task_id)

onMounted(async () => {
  await taskStore.loadTaskMessages(props.task_id)
  taskStore.connectWebSocket(props.task_id)
  const res = await getWriterSeque();
  writerSequence.value = Array.isArray(res.data) ? res.data : [];

  // 开始计时
  timer = setInterval(updateDuration, 1000)
  updateDuration() // 立即更新一次
})


onBeforeUnmount(() => {
  taskStore.closeWebSocket()
  // 清理计时器
  if (timer) {
    clearInterval(timer)
    timer = null
  }
})

</script>

<template>
  <div class="fixed inset-0">
    <ResizablePanelGroup direction="horizontal" class="h-full rounded-lg border">
      <ResizablePanel :default-size="40" class="h-full">
        <ChatArea :messages="taskStore.chatMessages" />
      </ResizablePanel>
      <ResizableHandle />
      <ResizablePanel :default-size="60" class="h-full min-w-0">
        <div class="flex h-full flex-col min-w-0">
          <Tabs default-value="modeler" class="w-full h-full flex flex-col">
            <!-- TODO: Agent 的状态 -->
            <div class="border-b px-4 py-1 flex justify-between">
              <div class="flex items-center gap-4">
                <div class="text-sm text-gray-600">
                  运行时长: <span class="font-mono text-blue-600">{{ runningDuration }}</span>
                </div>
                <TabsList>
                  <TabsTrigger value="modeler" class="text-sm">
                    ModelerAgent
                  </TabsTrigger>
                  <TabsTrigger value="coder" class="text-sm">
                    CoderAgent
                  </TabsTrigger>
                  <TabsTrigger value="writer" class="text-sm">
                    WriterAgent
                  </TabsTrigger>
                </TabsList>
              </div>
              <!--  TODO: 其他选项 -->

              <div class="flex justify-end gap-2 items-center">
                <Button @click="taskStore.downloadMessages" class="flex justify-end">
                  下载消息
                </Button>

                <FilesSheet />

              </div>

            </div>

            <TabsContent value="modeler" class="flex-1 p-1 min-w-0 h-full overflow-hidden">
              <ModelerEditor />
            </TabsContent>

            <TabsContent value="coder" class="flex-1 p-1 min-w-0 h-full overflow-hidden">
              <CoderEditor />
            </TabsContent>

            <TabsContent value="writer" class="flex-1 p-1 min-w-0 h-full overflow-hidden">
              <WriterEditor :messages="taskStore.writerMessages" :writerSequence="writerSequence" />
            </TabsContent>
          </Tabs>
        </div>
      </ResizablePanel>
    </ResizablePanelGroup>

  </div>
</template>

<style scoped></style>
