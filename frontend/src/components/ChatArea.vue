<script setup lang="ts">
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import type { Message } from "@/utils/response";
import { Send } from "lucide-vue-next";
import { ref } from "vue";
import Bubble from "./Bubble.vue";
import SystemMessage from "./SystemMessage.vue";

// ---- Props ----

const props = defineProps<{ messages: Message[] }>();

// ---- Reactive State ----

const inputValue = ref("");
const inputRef = ref<HTMLInputElement | null>(null);
const scrollRef = ref<HTMLDivElement | null>(null);

// ---- Methods ----

/** 发送消息（本地处理） */
const sendMessage = () => {
	if (!inputValue.value.trim()) return;
	inputValue.value = "";
	inputRef.value?.focus();
};
</script>

<template>
  <div class="flex h-full flex-col p-3">
    <div ref="scrollRef" class="flex-1 overflow-y-auto">
      <template v-for="message in props.messages" :key="message.id">
        <div class="mb-3">
          <!-- 用户消息 -->
          <Bubble v-if="message.msg_type === 'user'" type="user" :content="message.content || ''" />
          <!-- agent 消息（CoderAgent/WriterAgent，只显示 content） -->
          <Bubble v-else-if="message.msg_type === 'agent'" type="agent" :agentType="message.agent_type"
            :content="message.content || ''" />
          <!-- 系统消息 -->
          <SystemMessage v-else-if="message.msg_type === 'system'" :content="message.content || ''"
            :type="message.type" />
        </div>
      </template>
    </div>
    <form class="w-full max-w-2xl mx-auto flex items-center gap-2 pt-4" @submit.prevent="sendMessage">
      <Input ref="inputRef" v-model="inputValue" type="text" placeholder="请输入消息..." class="flex-1" autocomplete="off" />
      <Button type="submit" :disabled="!inputValue.trim()">
        <Send />
      </Button>
    </form>
  </div>
</template>

<style scoped>
/* 自定义滚动条样式 */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  @apply bg-transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  @apply bg-gray-300 dark:bg-gray-600 rounded-full;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  @apply bg-gray-400 dark:bg-gray-500;
}
</style>