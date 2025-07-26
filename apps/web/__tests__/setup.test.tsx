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

    // Test heading
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent(
      'SpectraAI'
    );

    // Test description
    expect(
      screen.getByText('Advanced AI Assistant with Emotional Intelligence')
    ).toBeInTheDocument();

    // Test button
    expect(
      screen.getByRole('button', { name: 'Get Started' })
    ).toBeInTheDocument();
  });

  it('demonstrates testing library matchers', () => {
    render(<SampleComponent />);

    const button = screen.getByRole('button', { name: 'Get Started' });

    // Testing Library Jest DOM matchers
    expect(button).toBeInTheDocument();
    expect(button).toBeVisible();
    expect(button).toBeEnabled();
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
