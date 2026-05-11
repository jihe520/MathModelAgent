<template>
  <div class="container mx-auto px-4 py-12 max-w-7xl bg-slate-50">
    <!-- 顶部标题区域 -->
    <div class="text-center mb-10">
      <h1 class="text-5xl font-custom-bold mb-4">
        <span class="gradient-text">MathModelAgent</span>
      </h1>
      <p class="text-xl text-gray-600 max-w-3xl mx-auto">
        专为数学建模设计的智能助手，让复杂的数学建模工作变得简单高效
      </p>
    </div>

    <!-- Bento Grid 布局 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
      <!-- 主卖点卡片 - 跨越2列2行 -->
      <div class="bento-card bg-white p-8 shadow-md md:col-span-2 md:row-span-2">
        <h2 class="text-2xl font-semibold mb-4 text-b">数学建模的革命性突破</h2>
        <div class="space-y-6">
          <div class="flex items-start" v-for="(item, idx) in mainPoints" :key="idx">
            <div class="flex-shrink-0 mr-4">
              <div class="w-12 h-12 rounded-full gradient-bg flex items-center justify-center">
                <component :is="item.icon" class="w-6 h-6 text-white" />
              </div>
            </div>
            <div>
              <h3 class="text-xl font-semibold mb-1">{{ item.title }}</h3>
              <p class="text-gray-600">{{ item.desc }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 核心功能卡片 -->
      <div class="bento-card bg-white p-6 shadow-md md:col-span-2">
        <div class="flex items-center mb-4">
          <Sparkles class="w-6 h-6 text-light-purple mr-2" />
          <h2 class="text-xl font-semibold">核心功能</h2>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div class="flex items-start" v-for="(item, idx) in coreFeatures" :key="idx">
            <component :is="item.icon" class="w-5 h-5 text-deep-purple mr-2 mt-0.5" />
            <p class="text-sm text-gray-600">{{ item.text }}</p>
          </div>
        </div>
      </div>

      <!-- 多智能体架构卡片 -->
      <div class="bento-card bg-white p-6 shadow-md">
        <div class="flex items-center mb-4">
          <Cpu class="w-6 h-6 text-light-purple mr-2" />
          <h2 class="text-xl font-semibold">多智能体系统</h2>
        </div>
        <div class="flex flex-col space-y-3">
          <div class="bg-gray-50 p-2 rounded-lg" v-for="(item, idx) in agents" :key="idx">
            <p class="text-sm font-medium">{{ item.role }}</p>
            <p class="text-xs text-gray-500">{{ item.desc }}</p>
          </div>
        </div>
      </div>

      <!-- 技术支持卡片 -->
      <div class="bento-card bg-white p-6 shadow-md">
        <div class="flex items-center mb-4">
          <CheckCircle class="w-6 h-6 text-light-purple mr-2" />
          <h2 class="text-xl font-semibold">技术支持</h2>
        </div>
        <div class="flex flex-wrap gap-2">
          <span v-for="(item, idx) in techs" :key="idx"
            class="px-3 py-1 bg-gray-100 rounded-full text-xs font-medium">{{ item }}</span>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <!-- 效率对比卡片 -->
      <div class="bento-card bg-white p-6 shadow-md">
        <div class="flex items-center mb-4">
          <BarChart2 class="w-6 h-6 text-light-purple mr-2" />
          <h2 class="text-xl font-semibold">效率提升</h2>
        </div>
        <div class="space-y-4">
          <div>
            <div class="flex justify-between mb-1">
              <span class="text-sm font-medium">传统方法</span>
              <span class="text-sm font-medium">72小时</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2.5">
              <div class="bg-gray-400 h-2.5 rounded-full" style="width: 100%"></div>
            </div>
          </div>
          <div>
            <div class="flex justify-between mb-1">
              <span class="text-sm font-medium">MathModelAgent</span>
              <span class="text-sm font-medium">1小时</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2.5">
              <div class="gradient-bg h-2.5 rounded-full" style="width: 1.4%"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 未来规划卡片 -->
      <div class="bento-card bg-white p-6 shadow-md">
        <div class="flex items-center mb-4">
          <Calendar class="w-6 h-6 text-light-purple mr-2" />
          <h2 class="text-xl font-semibold">未来规划</h2>
        </div>
        <ul class="space-y-2 text-sm text-gray-600">
          <li class="flex items-start" v-for="(item, idx) in plans" :key="idx">
            <Check class="w-4 h-4 text-deep-purple mr-2 mt-0.5" />
            <span>{{ item }}</span>
          </li>
        </ul>
      </div>

      <!-- CTA卡片 -->
      <div class="bento-card bg-gray-900 p-6 shadow-md text-white">
        <h2 class="text-xl font-semibold mb-4">立即开启您的建模之旅</h2>
        <p class="text-gray-300 mb-6">体验革命性的数学建模助手，节省时间，提高效率</p>
        <button class="w-full py-3 px-6 rounded-lg gradient-bg font-medium hover:opacity-90 transition-opacity"
          @click="router.push('/chat')">
          立即体验
        </button>
      </div>

    </div>

    <!-- 底部信息卡片 -->
    <div class="bento-card bg-white p-6 shadow-md">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <h3 class="text-lg font-semibold mb-2 gradient-text">关于我们</h3>
          <p class="text-sm text-gray-600">
            我们致力于通过人工智能技术简化数学建模过程，为学生和研究人员提供高效的解决方案。
          </p>
        </div>
        <div>
          <h3 class="text-lg font-semibold mb-2 gradient-text">适用场景</h3>
          <p class="text-sm text-gray-600">
            数学建模竞赛、学术研究、数据分析项目、科研论文写作、教学辅助工具。
          </p>
        </div>
        <div>
          <h3 class="text-lg font-semibold mb-2 gradient-text">联系我们</h3>
          <div class="flex space-x-4">
            <a :href=QQ_GROUP target="_blank" class="text-gray-400 hover:text-deep-purple">
              <svg t="1746706045339" class="icon" viewBox="0 0 1024 1024" version="1.1"
                xmlns="http://www.w3.org/2000/svg" p-id="4879" width="20" height="20">
                <path
                  d="M824.8 613.2c-16-51.4-34.4-94.6-62.7-165.3C766.5 262.2 689.3 112 511.5 112 331.7 112 256.2 265.2 261 447.9c-28.4 70.8-46.7 113.7-62.7 165.3-34 109.5-23 154.8-14.6 155.8 18 2.2 70.1-82.4 70.1-82.4 0 49 25.2 112.9 79.8 159-26.4 8.1-85.7 29.9-71.6 53.8 11.4 19.3 196.2 12.3 249.5 6.3 53.3 6 238.1 13 249.5-6.3 14.1-23.8-45.3-45.7-71.6-53.8 54.6-46.2 79.8-110.1 79.8-159 0 0 52.1 84.6 70.1 82.4 8.5-1.1 19.5-46.4-14.5-155.8z"
                  p-id="4880"></path>
              </svg>
            </a>
            <a :href=GITHUB_LINK class="text-gray-400 hover:text-deep-purple">
              <Github class="w-5 h-5" />
            </a>
            <a :href=TWITTER class="text-gray-400 hover:text-deep-purple">
              <Twitter class="w-5 h-5" />
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
	Award,
	BarChart2,
	Calendar,
	Check,
	CheckCircle,
	Clock,
	Code,
	Cpu,
	File,
	FileText,
	Github,
	Layers,
	Mail,
	Search,
	Sparkles,
	Twitter,
	Users,
	Wallet,
} from "lucide-vue-next";

import { GITHUB_LINK, QQ_GROUP, TWITTER } from "@/utils/const";
import { useRouter } from "vue-router";

const router = useRouter();

const mainPoints = [
	{
		icon: Clock,
		title: "3天 → 1小时",
		desc: "将传统3天的比赛时间缩短至1小时，极大提升工作效率",
	},
	{
		icon: Award,
		title: "获奖级建模论文",
		desc: "自动完成一份可以获奖级别的数学建模论文，无需人工干预",
	},
	{
		icon: FileText,
		title: "完整解决方案",
		desc: "从问题分析到论文提交，一站式解决数学建模全流程",
	},
];

const coreFeatures = [
	{ icon: Search, text: "自动分析问题与数学建模" },
	{ icon: Code, text: "本地代码解释器" },
	{ icon: File, text: "排版完整的论文生成" },
	{ icon: Users, text: "多智能体协作系统" },
	{ icon: Layers, text: "多种LLM模型支持" },
	{ icon: Wallet, text: "低成本Agentless架构" },
];

const agents = [
	{ role: "建模手", desc: "负责数学建模与分析" },
	{ role: "代码手", desc: "编写代码与反思优化" },
	{ role: "论文手", desc: "生成符合规范的论文" },
];

const techs = [
	"R语言",
	"MATLAB",
	"LaTeX模板",
	"视觉模型",
	"文献引用",
	"流程图绘制",
	"英文支持",
	"美赛适配",
];

const plans = [
	"更多数学建模测试案例支持",
	"引入用户交互（选择模型，重写等）",
	"代码解释器接入云端（e2b等供应商）",
];
</script>

<style scoped>
.gradient-text {
  background: linear-gradient(to right, #C084FC, #7E22CE);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.gradient-bg {
  background: linear-gradient(to right, #C084FC, #7E22CE);
}

.bento-card {
  border-radius: 20px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.bento-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}
</style>