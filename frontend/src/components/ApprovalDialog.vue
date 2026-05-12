<script setup lang="ts">
import { Button } from "@/components/ui/button";
import {
	Dialog,
	DialogContent,
	DialogFooter,
	DialogHeader,
	DialogTitle,
} from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";
import { ref, computed, onUnmounted } from "vue";

// ---- Props ----

/** 审批消息数据 */
interface ApprovalData {
	checkpoint_id: string;
	prompt: Record<string, unknown>;
	options: string[];
	timeout: number;
}

// ---- State ----

const showDialog = ref(false);
const approvalData = ref<ApprovalData | null>(null);
const editContent = ref("");
const showEditArea = ref(false);
const showAskArea = ref(false);
const askContent = ref("");
const remainingSeconds = ref(0);

let resolvePromise: ((value: { action: string; content?: unknown }) => void) | null = null;
let countdownTimer: ReturnType<typeof setInterval> | null = null;

// ---- Computed ----

const promptDisplay = computed(() => {
	if (!approvalData.value) return "";
	const p = approvalData.value.prompt;
	if (p.step) return `步骤: ${p.step}`;
	if (p.subtask) return `子任务: ${p.subtask}`;
	return JSON.stringify(p, null, 2);
});

const promptDetail = computed(() => {
	if (!approvalData.value) return "";
	const p = approvalData.value.prompt;
	// 显示关键内容摘要
	if (p.questions) return JSON.stringify(p.questions, null, 2).slice(0, 500);
	if (p.solutions) return JSON.stringify(p.solutions, null, 2).slice(0, 500);
	if (p.code_response) return String(p.code_response).slice(0, 500);
	if (p.summary) return String(p.summary).slice(0, 500);
	return "";
});

// ---- Methods ----

/** 打开审批对话框 */
function open(data: ApprovalData): Promise<{ action: string; content?: unknown }> {
	approvalData.value = data;
	editContent.value = "";
	askContent.value = "";
	showEditArea.value = false;
	showAskArea.value = false;
	showDialog.value = true;
	remainingSeconds.value = data.timeout;

	// 启动倒计时
	if (countdownTimer) clearInterval(countdownTimer);
	countdownTimer = setInterval(() => {
		remainingSeconds.value = Math.max(0, remainingSeconds.value - 1);
		if (remainingSeconds.value <= 0) {
			handleAction("confirm");
		}
	}, 1000);

	return new Promise((resolve) => {
		resolvePromise = resolve;
	});
}

/** 处理用户决策 */
function handleAction(action: string) {
	cleanup();
	showDialog.value = false;

	const result: { action: string; content?: unknown } = { action };

	if (action === "edit" && editContent.value) {
		try {
			result.content = JSON.parse(editContent.value);
		} catch {
			result.content = editContent.value;
		}
	} else if (action === "ask" && askContent.value) {
		result.content = askContent.value;
	}

	resolvePromise?.(result);
	resolvePromise = null;
}

/** 清理定时器 */
function cleanup() {
	if (countdownTimer) {
		clearInterval(countdownTimer);
		countdownTimer = null;
	}
}

onUnmounted(cleanup);

// ---- Expose ----

defineExpose({ open });
</script>

<template>
  <Dialog v-model:open="showDialog">
    <DialogContent class="max-w-lg">
      <DialogHeader>
        <DialogTitle>需要您的审批</DialogTitle>
      </DialogHeader>

      <div class="space-y-4 py-2">
        <!-- 检查点信息 -->
        <div class="rounded-md bg-muted p-3">
          <p class="text-sm font-medium">{{ promptDisplay }}</p>
          <pre v-if="promptDetail" class="mt-2 max-h-40 overflow-auto text-xs text-muted-foreground whitespace-pre-wrap">{{ promptDetail }}</pre>
        </div>

        <!-- 倒计时 -->
        <div class="text-sm text-muted-foreground text-center">
          <span v-if="remainingSeconds > 0">
            {{ remainingSeconds }}秒后自动继续
          </span>
          <span v-else class="text-orange-500">超时，自动继续...</span>
        </div>

        <!-- 编辑区域 -->
        <div v-if="showEditArea" class="space-y-2">
          <p class="text-sm text-muted-foreground">请输入修改后的内容（JSON 或文本）:</p>
          <Textarea v-model="editContent" rows="6" placeholder="输入修改后的内容..." />
        </div>

        <!-- 追问区域 -->
        <div v-if="showAskArea" class="space-y-2">
          <p class="text-sm text-muted-foreground">请输入补充信息:</p>
          <Textarea v-model="askContent" rows="3" placeholder="输入补充信息..." />
        </div>
      </div>

      <DialogFooter class="flex flex-wrap gap-2">
        <Button v-if="!showEditArea && !showAskArea" variant="default" @click="handleAction('confirm')">
          确认继续
        </Button>
        <Button v-if="!showEditArea && !showAskArea" variant="outline" @click="showEditArea = true">
          修改内容
        </Button>
        <Button v-if="!showEditArea && !showAskArea" variant="outline" @click="handleAction('regenerate')">
          重新生成
        </Button>
        <Button v-if="!showEditArea && !showAskArea" variant="outline" @click="showAskArea = true">
          追问
        </Button>
        <Button v-if="!showEditArea && !showAskArea" variant="ghost" @click="handleAction('skip')">
          跳过审核
        </Button>
        <Button v-if="!showEditArea && !showAskArea" variant="destructive" @click="handleAction('abort')">
          中止任务
        </Button>

        <!-- 编辑/追问确认 -->
        <Button v-if="showEditArea" variant="default" @click="handleAction('edit')">
          提交修改
        </Button>
        <Button v-if="showEditArea" variant="ghost" @click="showEditArea = false">
          取消
        </Button>
        <Button v-if="showAskArea" variant="default" @click="handleAction('ask')">
          发送追问
        </Button>
        <Button v-if="showAskArea" variant="ghost" @click="showAskArea = false">
          取消
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
