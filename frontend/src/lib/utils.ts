import type { Updater } from "@tanstack/vue-table";
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import type { Ref } from "vue";

/** 合并 Tailwind CSS 类名 */
export function cn(...inputs: ClassValue[]) {
	return twMerge(clsx(inputs));
}

/** 更新 TanStack Table 的值 */
// biome-ignore lint/suspicious/noExplicitAny: Updater 泛型约束需要 any
export function valueUpdater<T extends Updater<any>>(
	updaterOrValue: T,
	ref: Ref,
) {
	ref.value =
		typeof updaterOrValue === "function"
			? updaterOrValue(ref.value)
			: updaterOrValue;
}
