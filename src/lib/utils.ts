import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

function toCamelCaseKey(str: string): string {
  return str.replace(/_([a-z0-9])/g, (_, char) => char.toUpperCase())
}

export function snakeToCamel<T = any>(obj: any): T {
  if (obj === null || obj === undefined) return obj as T
  if (Array.isArray(obj)) return obj.map(item => snakeToCamel(item)) as unknown as T
  if (typeof obj !== 'object' || obj instanceof Date) return obj as T
  const result: Record<string, any> = {}
  for (const key of Object.keys(obj)) {
    result[toCamelCaseKey(key)] = snakeToCamel(obj[key])
  }
  return result as T
}

