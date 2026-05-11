<script setup lang="ts">
import NotebookArea from "@/components/NotebookArea.vue";
</script>

<template>
  <div class="h-full flex flex-col p-4">
    <div class="h-full bg-white rounded-lg border shadow-sm">
      <div class="border-b px-4 py-3">
        <h2 class="text-lg font-semibold text-gray-900">代码执行</h2>
      </div>
      <div class="h-full pb-14">
        <NotebookArea class="h-full" />
      </div>
    </div>
  </div>
</template>

<style scoped>
::-webkit-scrollbar {
  display: none;
  /* 或者 width: 0; height: 0; */
}
</style>
