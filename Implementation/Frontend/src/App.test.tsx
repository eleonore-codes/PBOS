import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { App } from "./App";

describe("App", () => {
  it("renders the founder dashboard", () => {
    render(<App />);

    expect(screen.getByRole("main", { name: /founder dashboard/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /creatingreorganized/i })).toBeInTheDocument();
  });
});
