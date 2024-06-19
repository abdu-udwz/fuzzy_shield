export type TaskStatus = "queued" | "partial" | "completed";

export interface TaskRaw {
  task_id: string;
  created_at: string;
  collection: string;
  text: string;
  status: TaskStatus;

  designated_result: boolean;

  sqli: boolean;
  xss: boolean;

  hamming: boolean;
  hamming_sqli_score?: number;
  hamming_sqli_time?: number;
  hamming_sqli_cpu?: number;
  hamming_sqli_memory?: number;
  hamming_sqli_match?: string;

  hamming_xss_score?: number;
  hamming_xss_time?: number;
  hamming_xss_cpu?: number;
  hamming_xss_memory?: number;
  hamming_xss_match?: string;

  naive: boolean;
  naive_sqli_score?: number;
  naive_sqli_time?: number;
  naive_sqli_cpu?: number;
  naive_sqli_memory?: number;
  naive_sqli_match?: string;

  naive_xss_score?: number;
  naive_xss_time?: number;
  naive_xss_cpu?: number;
  naive_xss_memory?: number;
  naive_xss_match?: string;

  levenshtein_ratio: boolean;
  levenshtein_ratio_sqli_score?: number;
  levenshtein_ratio_sqli_time?: number;
  levenshtein_ratio_sqli_cpu?: number;
  levenshtein_ratio_sqli_memory?: number;
  levenshtein_ratio_sqli_match?: string;

  levenshtein_ratio_xss_score?: number;
  levenshtein_ratio_xss_time?: number;
  levenshtein_ratio_xss_cpu?: number;
  levenshtein_ratio_xss_memory?: number;
  levenshtein_ratio_xss_match?: string;

  levenshtein_sort: boolean;
  levenshtein_sort_sqli_score?: number;
  levenshtein_sort_sqli_time?: number;
  levenshtein_sort_sqli_cpu?: number;
  levenshtein_sort_sqli_memory?: number;
  levenshtein_sort_sqli_match?: string;

  levenshtein_sort_xss_score?: number;
  levenshtein_sort_xss_time?: number;
  levenshtein_sort_xss_cpu?: number;
  levenshtein_sort_xss_memory?: number;
  levenshtein_sort_xss_match?: string;

}

export type SocketUpdate = Pick<TaskRaw, 'task_id'> & Partial<Omit<TaskRaw, 'task_id'>>
