<script setup lang="ts">
import { ref } from 'vue'
import { Button } from '@/components/ui/button'
import { FileUp } from 'lucide-vue-next'
import { Textarea } from '@/components/ui/textarea'
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import FileConfirmDialog from './FileConfirmDialog.vue'
import { submitModelingTask } from '@/apis/submitModelingApi'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Rocket } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { useTaskStore } from '@/stores/task'
import { useToast } from '@/components/ui/toast'
import { useApiKeyStore } from '@/stores/apiKeys'
import { saveApiConfig } from '@/apis/apiKeyApi'

const taskStore = useTaskStore()
const { toast } = useToast()
const apiKeyStore = useApiKeyStore()
const currentStep = ref(1)
const fileConfirmDialog = ref<InstanceType<typeof FileConfirmDialog> | null>(null)
const fileUploaded = ref(true)

// 表单数据
const uploadedFiles = ref<File[]>([])
const question = ref('')
const selectedOptions = ref({
  template: '国赛',
  language: '中文',
  format: 'Markdown',
})

const selectConfig = [
  {
    key: '模板',
    label: '选择模板',
    options: ['国赛', '美赛'],
  },
  {
    key: '语言',
    label: '选择语言',
    options: ['中文', '英文'],
  },
  {
    key: '格式',
    label: '选择格式',
    options: ['Markdown', 'LaTeX'],
  },
]

// 添加状态控制
const showUploadSuccess = ref(false)

// 提交任务
const showSubmitSuccess = ref(false)

const taskId = ref<string | null>(null)

// 添加 fileInput 的类型声明
const fileInput = ref<HTMLInputElement | null>(null)

const nextStep = () => {
  if (currentStep.value < 2)
    currentStep.value++
}

const prevStep = () => {
  if (currentStep.value > 1)
    currentStep.value--
}

// 修改文件上传处理
const handleFileUpload = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files.length > 0) {
    uploadedFiles.value = Array.from(input.files)
    fileUploaded.value = true
    showUploadSuccess.value = true // 显示提示
    setTimeout(() => {
      showUploadSuccess.value = false // 3秒后自动隐藏
    }, 1000)
  }
}

const router = useRouter()


const handleSubmit = async () => {
  try {

    if (apiKeyStore.isEmpty) {
      toast({
        title: '请先配置 API Key',
        description: '在侧边栏 -> 头像 -> API Key 中配置 API Key',
        variant: 'destructive',
      })
      return
    }

    // 保存 API Key
    await saveApiConfig({
      coordinator: apiKeyStore.coordinatorConfig,
      modeler: apiKeyStore.modelerConfig,
      coder: apiKeyStore.coderConfig,
      writer: apiKeyStore.writerConfig,
      openalex_email: apiKeyStore.openalexEmail
    })

    if (uploadedFiles.value.length === 0) {
      if (!fileConfirmDialog.value) return
      
      const shouldContinue = await fileConfirmDialog.value.openConfirmDialog()
      
      if (!shouldContinue) {
        toast({
          title: '请先上传文件',
          description: '请先上传文件',
          variant: 'destructive',
        })
        return
      }
    }
    console.log(selectedOptions.value)
    console.log(question.value)
    console.log(uploadedFiles.value)
    const response = await submitModelingTask(
      {
        ques_all: question.value,
        comp_template: selectedOptions.value.template,
        format_output: selectedOptions.value.format
      },
      uploadedFiles.value
    )

    taskId.value = response?.data?.task_id ?? null
    taskStore.addUserMessage(question.value)

    showSubmitSuccess.value = true
    setTimeout(() => {
      showSubmitSuccess.value = false // 3秒后自动隐藏
    }, 3000)
    router.push(`/task/${taskId.value}`)
    toast({
      title: '任务提交成功',
      description: '任务提交成功，编号为：' + taskId.value,
    })
  } catch (error) {
    console.error('任务提交失败:', error)
    toast({
      title: '任务提交失败',
      description: '请检查 API Key 是否正确',
      variant: 'destructive',
    })
  }
}
</script>

<template>
  <div class="w-full max-w-xl mx-auto relative">
    <!-- 使用 Alert 组件 -->
    <Transition name="fade">
      <div v-if="showUploadSuccess" class="fixed top-4 right-4 z-50">
        <Alert>
          <Rocket class="h-4 w-4" />
          <AlertTitle>文件上传成功！</AlertTitle>
          <AlertDescription>
            已成功上传 {{ uploadedFiles.length }} 个文件，请继续下一步操作。
          </AlertDescription>
        </Alert>
      </div>
    </Transition>

    <Transition name="fade">
      <div v-if="showSubmitSuccess" class="fixed top-4 right-4 z-50">
        <Alert>
          <Rocket class="h-4 w-4" />
          <AlertTitle>任务提交成功！</AlertTitle>
          <AlertDescription>
            任务提交成功，编号为：{{ taskId }}。
          </AlertDescription>
        </Alert>
      </div>
    </Transition>

    <div class="border rounded-lg shadow-sm">
      <!-- Step 1: File Upload -->
      <div v-if="currentStep === 1" class="p-6">
        <div
          class="border-2 border-dashed rounded-lg p-8 text-center hover:border-primary/50 transition-colors cursor-pointer"
          @click="() => fileInput?.click()">
          <input type="file" ref="fileInput" class="hidden" @change="handleFileUpload" accept=".txt,.csv,.xlsx"
            multiple>
          <div class="mx-auto w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
            <FileUp class="w-6 h-6 text-primary" />
          </div>
          <div>
            <p class="text-lg font-medium">拖拽数据集到此处或点击上传</p>
            <p class="text-sm text-muted-foreground mt-1">
              支持 .txt, .csv, .xlsx 等格式文件（可多选）
            </p>
            <div v-if="uploadedFiles.length > 0" class="text-sm text-green-600 mt-1">
              已上传文件:
              <ul>
                <li v-for="(file, index) in uploadedFiles" :key="index">
                  {{ file.name }}
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div class="mt-4 flex justify-end">
          <Button :disabled="!fileUploaded" @click="nextStep" size="sm">
            下一步
          </Button>
        </div>
      </div>

      <!-- Step 2: Question Input -->
      <div v-if="currentStep === 2" class="p-6">
        <div class="space-y-4">
          <div class="space-y-1">
            <h4 class="text-sm font-medium mb-2">粘贴完整题目</h4>
            <Textarea v-model="question" placeholder="PDF 中完整题目背景和多个小问" class="min-h-[120px]" />
          </div>

          <div class="grid grid-cols-3 gap-3">
            <div v-for="item in selectConfig" :key="item.key">
              <Select v-model="selectedOptions[item.key.toLowerCase() as keyof typeof selectedOptions]"
                :defaultValue="item.options[0].toLowerCase()">
                <SelectTrigger class="h-9">
                  <SelectValue :placeholder="item.label" />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectLabel>{{ item.key }}</SelectLabel>
                    <SelectItem v-for="option in item.options" :key="option" :value="option.toLowerCase()">
                      {{ option }}
                    </SelectItem>
                  </SelectGroup>
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>
        <div class="mt-4 flex justify-between">
          <Button variant="outline" @click="prevStep" size="sm">
            上一步
          </Button>
          <Button @click="handleSubmit" size="sm">
            开始分析
          </Button>
        </div>
      </div>
    </div>
  </div>
  <FileConfirmDialog ref="fileConfirmDialog" />
</template>