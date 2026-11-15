import { useEffect, useState, type Dispatch, type SetStateAction } from 'react';

/** useState that remembers its value in localStorage (per browser). Falls back quietly if storage is blocked. */
export function useStoredState<T>(key: string, initial: T, isValid: (v: unknown) => boolean = () => true): [T, Dispatch<SetStateAction<T>>] {
  const [value, setValue] = useState<T>(() => {
    try {
      const raw = localStorage.getItem(key);
      if (raw !== null) { const v: unknown = JSON.parse(raw); if (isValid(v)) return v as T; }
    } catch (e) { /* storage unavailable */ }
    return initial;
  });
  useEffect(() => { try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* ignore */ } }, [key, value]);
  return [value, setValue];
}
