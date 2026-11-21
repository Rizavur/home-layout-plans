/** Build number, injected by build.mjs (used to bust caches). */
declare const __BUILD__: string;

declare module '*.css';

/** Path tracer, loaded from the CDN through the import map on first use (see engine/photo.ts). */
declare module 'three-gpu-pathtracer';
