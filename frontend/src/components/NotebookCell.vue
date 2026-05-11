<script setup lang="ts">
import type { CodeCell, NoteCell, ResultCell } from "@/utils/interface";
import { renderMarkdown } from "@/utils/markdown";
import type { CodeExecutionResult } from "@/utils/response";

// ---- Props ----

defineProps<{
	cell: NoteCell;
}>();

// ---- Methods ----

/** 获取结果格式对应的 CSS 类 */
const getResultClass = (result: CodeExecutionResult) => {
	switch (result.res_type) {
		case "stdout":
			return "text-gray-600";
		case "stderr":
			return "text-orange-600";
		case "error":
			return "text-red-600";
		default:
			return "text-gray-800";
	}
};

/** 判断结果是否为图片格式 */
const isImageResult = (result: CodeExecutionResult) => {
	return (
		result.res_type === "result" &&
		["png", "jpeg", "svg"].includes(result.format as string)
	);
};

/** 判断结果是否为 LaTeX 格式 */
const isLatexResult = (result: CodeExecutionResult) => {
	return result.res_type === "result" && result.format === "latex";
};

/** 判断结果是否为 JSON 格式 */
const isJsonResult = (result: CodeExecutionResult) => {
	return result.res_type === "result" && result.format === "json";
};

/** 格式化 JSON 显示 */
const formatJson = (jsonString: string) => {
	try {
		const parsed = JSON.parse(jsonString);
		return JSON.stringify(parsed, null, 2);
	} catch (e) {
		return jsonString;
	}
};

/** 渲染 Markdown 内容 */
const renderMarkdownContent = (content: string) => {
	return renderMarkdown(content);
};

/** 类型守卫：判断是否为代码单元格 */
const isCodeCell = (cell: NoteCell): cell is CodeCell => {
	return cell.type === "code";
};

/** 类型守卫：判断是否为结果单元格 */
const isResultCell = (cell: NoteCell): cell is ResultCell => {
	return cell.type === "result";
};
</script>

<template>
  <div :class="[
    'bg-white rounded-lg shadow-sm overflow-hidden',
    'border border-gray-200 hover:border-blue-300',
    cell.type === 'code' ? 'code-cell' : 'result-cell'
  ]">
    <!-- 单元格头部 -->
    <div
      class="px-3 py-1 flex items-center justify-between bg-gradient-to-r from-gray-50 to-white border-b border-gray-200">
      <div class="flex items-center space-x-2">
        <span :class="[
          'px-2 py-1 rounded text-xs font-medium',
          cell.type === 'code' ? 'bg-blue-50 text-blue-600' : 'bg-green-50 text-green-600'
        ]">
          {{ cell.type === 'code' ? 'Code' : 'Result' }}
        </span>
      </div>
    </div>

    <!-- 代码内容 -->
    <div class="relative">
      <!-- 代码单元格 -->
      <template v-if="isCodeCell(cell)">
        <div class="p-4 font-mono relative group">
          <pre class="text-sm overflow-x-auto"><code>{{ cell.content }}</code></pre>
        </div>
      </template>

      <!-- 结果单元格 -->
      <template v-else-if="isResultCell(cell)">
        <div class="px-4 py-3 bg-gray-50">
          <div class="text-xs font-medium text-gray-500 mb-2">输出:</div>
          
          <!-- 遍历所有执行结果 -->
          <div v-for="(result, index) in cell.code_results" :key="index" class="mb-2 last:mb-0">
            <!-- 标准输出/错误 -->
            <template v-if="result.res_type === 'stdout' || result.res_type === 'stderr'">
              <div :class="['font-mono whitespace-pre-wrap text-sm', getResultClass(result)]">
                {{ result.msg }}
              </div>
            </template>
            
            <!-- 执行错误 -->
            <template v-else-if="result.res_type === 'error'">
              <div class="text-sm text-red-600 font-mono whitespace-pre-wrap">
                <div class="font-bold">{{ result.name }}: {{ result.value }}</div>
                <div>{{ result.traceback }}</div>
              </div>
            </template>
            
            <!-- 执行结果 - 图片 (PNG, JPEG, SVG) -->
            <template v-else-if="isImageResult(result)">
              <img :src="`data:image/${result.format};base64,${result.msg}`" 
                   class="max-w-full rounded-lg shadow-sm" />
            </template>
            
            <!-- 执行结果 - HTML -->
            <template v-else-if="result.res_type === 'result' && result.format === 'html'">
              <div class="prose prose-sm max-w-none" v-html="result.msg || ''"></div>
            </template>
            
            <!-- 执行结果 - Markdown -->
            <template v-else-if="result.res_type === 'result' && result.format === 'markdown'">
              <div class="prose prose-sm max-w-none" v-html="renderMarkdownContent(result.msg || '')"></div>
            </template>
            
            <!-- 执行结果 - LaTeX -->
            <template v-else-if="isLatexResult(result)">
              <div class="katex-display" v-html="result.msg || ''"></div>
            </template>
            
            <!-- 执行结果 - JSON -->
            <template v-else-if="isJsonResult(result)">
              <pre class="text-sm bg-gray-50 p-2 rounded overflow-x-auto">{{ formatJson(result.msg || '') }}</pre>
            </template>
            
            <!-- 执行结果 - 默认文本 -->
            <template v-else>
              <div class="text-sm text-gray-600 font-mono whitespace-pre-wrap">
                {{ result.msg }}
              </div>
            </template>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
/* 代码样式 */
.code-cell pre {
  background-color: rgb(249 250 251);
  border-radius: 0.375rem;
  padding: 0.5rem;
}

.code-cell code {
  color: rgb(31 41 55);
}

/* 结果样式 */
.result-cell {
  margin-top: -0.25rem;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>