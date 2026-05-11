<script setup lang="ts">
import { Button } from "@/components/ui/button";
import { ref } from "vue";
import { useRouter } from "vue-router";

import { exampleAPI } from "@/apis/commonApi";
import mcmCupC from "@/assets/example/2024高教杯C题.png";
import wuyiCupC from "@/assets/example/2025五一杯C题.png";
import huashuCupC from "@/assets/example/华数杯2023年C题.png";

// ---- Types ----

/** 建模样例数据结构 */
interface ModelingExample {
	id: number;
	title: string;
	source: string;
	description: string;
	tags: string[];
	problemText: string;
	image: string;
}

// ---- Reactive State ----

const router = useRouter();

/** 样例列表 */
const examples = ref<ModelingExample[]>([
	{
		id: 1,
		title: "母亲身心健康对婴儿成长的影响",
		source: "2023华数杯C题",
		description: "研究母亲身心健康对婴儿成长的影响",
		tags: ["分类问题", "成长", "健康"],
		problemText: "给定母亲身心健康数据，建立一个预测模型，预测婴儿成长情况。",
		image: huashuCupC,
	},
	{
		id: 2,
		title: "社交媒体平台用户分析问题",
		source: "2025五一杯C题",
		description: "分析社交媒体平台用户行为特征",
		tags: ["社交媒体", "用户行为"],
		problemText: "分析社交媒体平台用户行为特征，构建用户画像模型。",
		image: wuyiCupC,
	},
	{
		id: 3,
		title: "农作物的种植策略",
		source: "2024高教杯C题",
		description: "研究农作物的种植策略",
		tags: ["种植策略", "农作物", "生长"],
		problemText:
			"研究农作物的种植策略，建立一个优化模型，使得农作物产量最大化。",
		image: mcmCupC,
	},
]);

/** 选择样例并跳转到任务创建步骤 */
const selectExample = async (example: ModelingExample) => {
	const res = await exampleAPI(example.id.toString(), example.source);
	const task_id = res?.data?.task_id;
	router.push(`/task/${task_id}`);
};
</script>

<template>
  <div class="mt-8 mb-12">
    <h2 class="text-xl font-medium mb-4">样例解析</h2>
    <p class="text-sm text-muted-foreground mb-6">浏览历年数模竞赛优秀案例，快速开始你的建模任务</p>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="example in examples" :key="example.id"
        class="border rounded-lg overflow-hidden hover:shadow-md transition-shadow group">
        <!-- 题目缩略图 -->
        <div class="relative h-48 overflow-hidden bg-muted">
          <img :src="example.image" alt="题目缩略图"
            class="w-full h-full object-cover object-top group-hover:scale-105 transition-transform duration-300" />
          <div
            class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
            <Button variant="secondary" size="sm" @click="selectExample(example)">
              查看详情
            </Button>
          </div>
        </div>

        <!-- 题目信息 -->
        <div class="p-4">
          <div class="flex justify-between items-start mb-2">
            <h3 class="font-medium line-clamp-2">{{ example.title }}</h3>
            <span class="text-xs px-2 py-0.5 bg-primary/10 text-primary rounded-full">
              {{ example.tags[0] }}
            </span>
          </div>
          <p class="text-xs text-muted-foreground mb-2">{{ example.source }}</p>
          <p class="text-sm text-muted-foreground mb-4 line-clamp-2">{{ example.description }}</p>

          <!-- 标签 -->
          <div class="flex flex-wrap gap-1 mb-4">
            <span v-for="(tag, _) in example.tags.slice(1)" :key="tag"
              class="px-2 py-0.5 bg-muted text-muted-foreground rounded-full text-xs">
              {{ tag }}
            </span>
          </div>

          <!-- 按钮 -->
          <Button variant="default" size="sm" class="w-full" @click="selectExample(example)">
            使用该案例
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>