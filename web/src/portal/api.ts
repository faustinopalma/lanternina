import type { Photograph } from "@/api/types";
import { config } from "@/config";

export class PortalError extends Error {
  constructor(public status: number, public detail: string) { super(detail); }
}

export interface PortalPage {
  photos: Photograph[];
  page: number;
  pages: number;
  total: number;
}

export interface PortalApi {
  me(): Promise<{ id: string; email: string }>;
  accept(token: string): Promise<void>;
  photos(page: number): Promise<PortalPage>;
  content(id: string): Promise<Blob>;
  send(id: string, photo: Blob): Promise<Photograph>;
  delete(id: string): Promise<void>;
}

export function portalApi(bearer: () => Promise<string | null>): PortalApi {
  async function request(path: string, options: RequestInit = {}) {
    const token = await bearer();
    if (!token) throw new PortalError(401, "signin_required");
    const response = await fetch(`${config.apiBase}/api/portal${path}`, {
      ...options, cache: "no-store", signal: AbortSignal.timeout(60_000),
      headers: { ...options.headers, Authorization: `Bearer ${token}` },
    });
    if (!response.ok) {
      const body = await response.json().catch(() => ({}));
      throw new PortalError(response.status, body.detail ?? "request_failed");
    }
    return response;
  }
  return {
    me: async () => (await request("/me")).json(),
    accept: async (token) => {
      await request("/accept", { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token }) });
    },
    photos: async (page) => (await request(`/photos?page=${page}`)).json(),
    content: async (id) => (await request(`/photos/${id}/content`)).blob(),
    send: async (id, photo) => (await request(`/photos/${id}`, {
      method: "POST", headers: { "Content-Type": "image/jpeg" }, body: photo,
    })).json(),
    delete: async (id) => { await request(`/photos/${id}`, { method: "DELETE" }); },
  };
}

export async function preparePhoto(file: File): Promise<Blob> {
  if (file.size > 25_000_000 || !["image/jpeg", "image/png", "image/webp"].includes(file.type)) {
    throw new Error("unsupported_photo");
  }
  const source = await createImageBitmap(file);
  try {
    const scale = Math.min(1, 1600 / source.width, 1200 / source.height);
    const canvas = document.createElement("canvas");
    canvas.width = Math.max(1, Math.round(source.width * scale));
    canvas.height = Math.max(1, Math.round(source.height * scale));
    const context = canvas.getContext("2d");
    if (!context) throw new Error("canvas_unavailable");
    context.drawImage(source, 0, 0, canvas.width, canvas.height);
    return await new Promise<Blob>((resolve, reject) => canvas.toBlob(
      (blob) => blob ? resolve(blob) : reject(new Error("photo_conversion_failed")), "image/jpeg", 0.85,
    ));
  } finally { source.close(); }
}