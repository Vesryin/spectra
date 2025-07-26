// Placeholder UI components for SpectraAI
import * as React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  asChild?: boolean;
  variant?: string;
  size?: string;
}

export const Button = ({
  children,
  asChild,
  variant,
  size,
  ...props
}: ButtonProps) => <button {...props}>{children}</button>;

export const Card = ({
  children,
  ...props
}: { children: React.ReactNode } & React.HTMLAttributes<HTMLDivElement>) => (
  <div {...props}>{children}</div>
);

export const CardContent = ({
  children,
  ...props
}: { children: React.ReactNode } & React.HTMLAttributes<HTMLDivElement>) => (
  <div {...props}>{children}</div>
);

export const CardDescription = ({
  children,
  ...props
}: {
  children: React.ReactNode;
} & React.HTMLAttributes<HTMLParagraphElement>) => <p {...props}>{children}</p>;

export const CardHeader = ({
  children,
  ...props
}: { children: React.ReactNode } & React.HTMLAttributes<HTMLDivElement>) => (
  <div {...props}>{children}</div>
);

export const CardTitle = ({
  children,
  ...props
}: {
  children: React.ReactNode;
} & React.HTMLAttributes<HTMLHeadingElement>) => <h3 {...props}>{children}</h3>;
