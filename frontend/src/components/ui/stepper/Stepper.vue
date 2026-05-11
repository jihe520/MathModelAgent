<script lang="ts" setup>
import { cn } from "@/lib/utils";
import type { StepperRootEmits, StepperRootProps } from "reka-ui";
import { StepperRoot, useForwardPropsEmits } from "reka-ui";

import { type HTMLAttributes, computed } from "vue";

const props = defineProps<
	StepperRootProps & { class?: HTMLAttributes["class"] }
>();
const emits = defineEmits<StepperRootEmits>();

const delegatedProps = computed(() => {
	const { class: _, ...delegated } = props;

	return delegated;
});

const forwarded = useForwardPropsEmits(delegatedProps, emits);
</script>

<template>
  <StepperRoot
    v-slot="slotProps"
    :class="cn(
      'flex gap-2',
      props.class,
    )"
    v-bind="forwarded"
  >
    <slot v-bind="slotProps" />
  </StepperRoot>
</template>
