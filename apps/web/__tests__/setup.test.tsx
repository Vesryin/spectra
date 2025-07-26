/**
 * Sample test for SpectraAI Frontend
 * Demonstrates testing setup and best practices
 */

import { render, screen } from '@testing-library/react';
import { describe, it, expect } from '@jest/globals';

// Mock component for testing
const SampleComponent = () => {
  return (
    <div>
      <h1>SpectraAI</h1>
      <p>Advanced AI Assistant with Emotional Intelligence</p>
      <button>Get Started</button>
    </div>
  );
};

describe('SpectraAI Frontend Setup', () => {
  it('renders the sample component correctly', () => {
    render(<SampleComponent />);

    // Test basic rendering
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading.textContent).toBe('SpectraAI');

    const description = screen.getByText(
      'Advanced AI Assistant with Emotional Intelligence'
    );
    expect(description).toBeTruthy();

    const button = screen.getByRole('button', { name: /get started/i });
    expect(button).toBeTruthy();
  });

  it('demonstrates modern testing patterns', () => {
    render(<SampleComponent />);

    // Query tests
    const button = screen.getByRole('button');
    expect(button).toBeTruthy();
    expect(button.textContent).toBe('Get Started');

    // Multiple element tests
    const allText = screen.getAllByText(/spectra|ai|assistant/i);
    expect(allText.length).toBeGreaterThan(0);
  });
});

describe('Jest Configuration', () => {
  it('supports modern JavaScript features', () => {
    // Arrow functions
    const add = (a: number, b: number) => a + b;
    expect(add(2, 3)).toBe(5);

    // Template literals
    const name = 'SpectraAI';
    expect(`Welcome to ${name}`).toBe('Welcome to SpectraAI');

    // Destructuring
    const { length } = [1, 2, 3];
    expect(length).toBe(3);
  });

  it('supports async/await', async () => {
    const asyncFunction = async () => {
      return new Promise(resolve => {
        setTimeout(() => resolve('Done'), 10);
      });
    };

    const result = await asyncFunction();
    expect(result).toBe('Done');
  });
});
