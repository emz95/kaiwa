export interface Scenario {
  id: string; // UUID
  slug: string;
  name: string;
  description: string | null;
  order_index: number;
  is_active: boolean;
  created_at: string; // ISO datetime
}
