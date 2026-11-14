import { useEffect, useState } from 'react';

/** useState that remembers its value in localStorage (per browser). Falls back quietly if storage is blocked. */
export function useStoredState(key, initial, isValid = () => true) {
  const [value, setValue] = useState(() => {
    try {
      const raw = localStorage.getItem(key);
      if (raw !== null) { const v = JSON.parse(raw); if (isValid(v)) return v; }
    } catch (e) { /* storage unavailable */ }
    return initial;
  });
  useEffect(() => { try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* ignore */ } }, [key, value]);
  return [value, setValue];
}
