import "@testing-library/jest-dom/vitest";

// jsdom has no blob URLs. The gallery only needs a string it can put in `src`.
if (typeof URL.createObjectURL !== "function") {
  URL.createObjectURL = () => "blob:lanternina";
  URL.revokeObjectURL = () => undefined;
}
