<script setup lang="ts">


import AppSidebar from '@/components/AppSidebar.vue'
import UserStepper from '@/components/UserStepper.vue'
import ModelingExamples from '@/components/ModelingExamples.vue'
import { onMounted } from 'vue'
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from '@/components/ui/sidebar'
import { getHelloWorld } from '@/apis/commonApi'
onMounted(() => {
  getHelloWorld().then((res) => {
    console.log(res.data)
  })
})
</script>

<template>

  <SidebarProvider>
    <AppSidebar />
    <SidebarInset>
      <header class="flex h-16 shrink-0 items-center gap-2 px-4">
        <SidebarTrigger class="-ml-1" />
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

          <ModelingExamples />
        </div>
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>
