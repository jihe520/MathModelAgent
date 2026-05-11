<script setup lang="ts">
import Tree from "@/components/Tree.vue";
import {
	Sidebar,
	SidebarContent,
	SidebarFooter,
	SidebarGroup,
	SidebarProvider,
} from "@/components/ui/sidebar";
import { useTaskStore } from "@/stores/task";
import { File } from "lucide-vue-next";
import { computed, onMounted, ref } from "vue";

// ---- Reactive State ----

const taskStore = useTaskStore();
const isLoading = ref(true);

/** 从消息中提取最新的文件列表 */
const files = taskStore.files as string[];

// ---- Computed ----

/** 将文件列表转换为树形结构 */
const fileTree = computed(() => {
	isLoading.value = false;
	return files;
});

// ---- Lifecycle Hooks ----

onMounted(() => {
	setTimeout(() => {
		isLoading.value = false;
	}, 3000);
});

// ---- Methods ----

const handleFileClick = (file: string) => {
	console.log("File clicked:", file);
};

const handleFileDownload = (file: string) => {
	console.log("Download file:", file);
};
</script>

<template>
  <SidebarContent class="h-full">
    <SidebarGroup />
    <div class="h-full flex flex-col overflow-hidden">
      <div class="px-3 py-2 font-medium text-sm border-b">Files</div>
      <div class="flex-1 overflow-auto">
        <div v-if="isLoading" class="px-3 py-2 text-sm text-gray-500">
          加载中...
        </div>
        <div v-else-if="fileTree.length === 0" class="px-3 py-2 text-sm text-gray-500">
          暂无文件
        </div>
        <div v-else class="p-2">
          <Tree v-for="(item, index) in fileTree" :key="index" :item="item" @click="handleFileClick(item)"
            @download="handleFileDownload(item)" />
        </div>
      </div>
    </div>
    <SidebarGroup />
  </SidebarContent>
</template>
