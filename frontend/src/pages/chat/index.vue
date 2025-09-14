<script setup lang="ts">


import AppSidebar from '@/components/AppSidebar.vue'
import UserStepper from '@/components/UserStepper.vue'
import ModelingExamples from '@/components/ModelingExamples.vue'
import { onMounted, ref } from 'vue'
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from '@/components/ui/sidebar'
import { getHelloWorld } from '@/apis/commonApi'
import MoreDetail from '@/pages/chat/components/MoreDetail.vue'
import Button from '@/components/ui/button/Button.vue'
import ServiceStatus from '@/components/ServiceStatus.vue'
import { AppWindow, CircleEllipsis } from 'lucide-vue-next'
onMounted(() => {
  getHelloWorld().then((res) => {
    console.log(res.data)
  })
})


const isMoreDetailOpen = ref(false)

</script>

<template>

  <SidebarProvider>
    <MoreDetail v-model="isMoreDetailOpen" />
    <AppSidebar />
    <SidebarInset>
      <header class="flex h-16 shrink-0 items-center gap-2 px-4">
        <SidebarTrigger class="-ml-1" />
        <div class="flex justify-between w-full gap-2">
          <ServiceStatus />
          <div class="flex gap-2">
            <Button variant="outline" @click="isMoreDetailOpen = true">
              <CircleEllipsis />
              更多
            </Button>
            <a href="https://www.mathmodel.top/" target="_blank">
              <Button variant="outline">
                <AppWindow />
                官网
              </Button>
            </a>
          </div>
        </div>
      </header>

      <div class="py-5 px-4">
        <div class="space-y-6">
          <div class="text-center space-y-2 mb-10">
            <h1 class="text-2xl font-semibold">MathModelAgent</h1>
            <p class="text-muted-foreground">
              让 Agent 数学建模，代码编写，论文写作
            </p>
          </div>

          <UserStepper>
          </UserStepper>
          <div class="text-center text-xs text-muted-foreground mt-8">
            项目处于内测阶段，欢迎进群反馈
          </div>
          <ModelingExamples />
        </div>
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>
