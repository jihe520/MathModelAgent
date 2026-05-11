<script setup lang="ts">
import { cn } from "@/lib/utils";
import type { AgentType } from "@/utils/enum";
import { marked } from "marked";
import type { HTMLAttributes } from "vue";
import { computed } from "vue";

// ---- Props ----

interface BubbleProps {
	type: "agent" | "user";
	agentType?: AgentType;
	class?: HTMLAttributes["class"];
	content: string;
}

const props = withDefaults(defineProps<BubbleProps>(), {
	type: "user",
});

// ---- Computed ----

/** 渲染 Markdown 内容 */
const renderedContent = computed(() => {
	return marked.parse(props.content);
});
</script>

<template>
  <div :class="[
    'bubble',
    props.type === 'user' ? 'bubble-user' : '',
    props.type === 'agent' && props.agentType === 'CoderAgent' ? 'bubble-coder' : '',
    props.type === 'agent' && props.agentType === 'WriterAgent' ? 'bubble-writer' : '',
    props.class
  ]">
    <div class="flex flex-col gap-1 flex-1">
      <!-- 头像在上方 -->
      <span v-if="props.type === 'user'" class="text-2xl select-none mb-1">🧑</span>
      <span v-else-if="props.type === 'agent' && props.agentType === 'CoderAgent'"
        class="text-2xl select-none mb-1">👨‍💻</span>
      <span v-else-if="props.type === 'agent' && props.agentType === 'WriterAgent'"
        class="text-2xl select-none mb-1">✍️</span>
      <!-- 气泡内容在下方 -->
      <div :class="cn(
        'max-w-[80%] rounded-2xl px-4 py-2 text-sm',
        props.type === 'user'
          ? 'bg-primary text-primary-foreground prose-invert'
          : 'bg-muted text-foreground',
        'prose prose-sm prose-slate max-w-none'
      )">
        <div v-html="renderedContent"></div>
      </div>
    </div>
  </div>
</template>

<style>
.prose {
  @apply text-inherit;
}

.prose p {
  @apply my-1;
}

.prose p:not(:first-child) {
  @apply mt-1;
}

.prose h1,
.prose h2,
.prose h3,
.prose h4 {
  @apply my-1 font-semibold;
}

.prose h1 {
  @apply text-lg;
}

.prose h2 {
  @apply text-base;
}

.prose h3,
.prose h4 {
  @apply text-sm;
}

.prose ul,
.prose ol {
  @apply my-1 pl-4;
}

.prose ul {
  @apply list-disc;
}

.prose ol {
  @apply list-decimal;
}

.prose li {
  @apply my-0.5;
}

.prose code {
  @apply px-1 py-0.5 rounded bg-black/10 dark:bg-white/10;
}

.prose pre {
  @apply p-2 my-1 rounded bg-black/10 dark:bg-white/10 overflow-x-auto;
  max-width: 100%;
  width: 100%;
}

.prose pre code {
  @apply bg-transparent p-0;
  @apply overflow-y-auto;
  max-width: 100%;
  white-space: pre-wrap;
  word-break: break-word;
}

.prose blockquote {
  @apply my-1 pl-3 border-l-2 border-current opacity-80 italic;
}

.prose a {
  @apply underline underline-offset-2 opacity-80 hover:opacity-100;
}

.prose img {
  @apply my-1 rounded-lg;
}

.prose table {
  @apply my-1 w-full;
}

.prose thead {
  @apply border-b border-current opacity-20;
}

.prose th {
  @apply p-2 text-left font-semibold;
}

.prose td {
  @apply p-2 border-t border-current opacity-10;
}

.prose-invert {
  @apply text-primary-foreground;
}

/* 确保透明度样式不会被继承 */
.prose thead *,
.prose td * {
  @apply opacity-100;
}

.bubble {
  display: flex;
  flex: 1 1 0%;
}

.bubble-user {
  justify-content: flex-end;
}

.bubble-coder,
.bubble-writer {
  justify-content: flex-start;
}

/* 用户气泡颜色 */
.bubble-user .prose {
  background: #2563eb;
  /* 蓝色 */
  color: #fff;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.08);
  border: 1px solid #2563eb;
}

/* CoderAgent 气泡颜色 */
.bubble-coder .prose {
  background: #f1f5f9;
  /* 浅灰 */
  color: #0f172a;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.08);
}

/* WriterAgent 气泡颜色 */
.bubble-writer .prose {
  background: #fef9c3;
  /* 浅黄 */
  color: #92400e;
  box-shadow: 0 2px 8px rgba(251, 191, 36, 0.08);
}
</style>