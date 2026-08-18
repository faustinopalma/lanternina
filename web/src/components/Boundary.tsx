import { Component, type ReactNode } from "react";

/* A section that throws must not take the panel with it. Without this, one answer the
 * panel did not expect leaves a white page whose only way out is a reload — and the menu
 * goes with it, so the parent cannot even move somewhere else.
 *
 * A class, because this is the one thing React has no hook for.
 */
export class Boundary extends Component<
  { children: ReactNode; fallback: ReactNode; resetOn: string },
  { failed: boolean }
> {
  state = { failed: false };

  static getDerivedStateFromError() {
    return { failed: true };
  }

  componentDidUpdate(previous: { resetOn: string }) {
    // Moving to another section is the retry: the failed one is asked again on return.
    if (previous.resetOn !== this.props.resetOn && this.state.failed) {
      this.setState({ failed: false });
    }
  }

  render() {
    return this.state.failed ? this.props.fallback : this.props.children;
  }
}
