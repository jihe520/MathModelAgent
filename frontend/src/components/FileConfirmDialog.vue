<script setup lang="ts">
import { ref } from 'vue'
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'

// 控制弹窗显示
const showConfirmDialog = ref(false)
let resolvePromise: (value: boolean) => void

// 打开确认弹窗（返回Promise）
const openConfirmDialog = () => {
  showConfirmDialog.value = true
  return new Promise((resolve) => {
    resolvePromise = resolve
  })
}

// 处理确认操作
const handleConfirm = () => {
  showConfirmDialog.value = false
  resolvePromise(true) // 继续执行
}

// 处理取消操作
const handleCancel = () => {
  showConfirmDialog.value = false
  resolvePromise(false) // 返回上传文件
}

// 暴露方法给父组件
defineExpose({ openConfirmDialog })
</script>
<template>
  <!-- 确认弹窗 -->
  <Dialog v-model:open="showConfirmDialog">
    <DialogContent>
      <DialogHeader>
        <DialogTitle>确认操作</DialogTitle>
      </DialogHeader>
      <div class="py-4">
        <p class="text-gray-700">您尚未上传任何文件，确定要继续吗？</p>
      </div>
      <DialogFooter>
        <Button variant="outline" @click="handleCancel">去上传文件</Button>
        <Button @click="handleConfirm">继续操作</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>