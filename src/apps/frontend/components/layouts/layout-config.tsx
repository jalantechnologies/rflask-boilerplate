import React from 'react';

// Layout 1: Half image and half form
const HalfImageHalfFormLayout: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => (
  <div className="flex h-screen">
    {/* Left side: Image */}
    <div
      className="flex-1 bg-cover bg-center"
      style={{ backgroundImage: 'url(/assets/img/auth-background.jpg)' }}
    />
    {/* Right side: Form */}
    <div className="flex flex-1 items-start justify-start overflow-hidden p-4">
      <div className="w-full max-w-[600px] p-4">{children}</div>
    </div>
  </div>
);

// Layout 2: Full form (no image)
const FullFormLayout: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => (
  <div className="flex h-screen items-start justify-center overflow-hidden p-4">
    <div className="w-full max-w-[600px] p-4">{children}</div>
  </div>
);

// Layout 3: Centered form with semi-transparent background image
const CenteredFormWithBackgroundLayout: React.FC<{
  children: React.ReactNode;
}> = ({ children }) => (
  <div
    className="flex h-screen items-start justify-center overflow-hidden"
    style={{
      backgroundImage: 'url(/assets/img/auth-background.jpg)',
      backgroundSize: 'cover',
      backgroundPosition: 'center',
    }}
  >
    {/* Semi-transparent overlay */}
    <div className="absolute inset-0 bg-black/50"></div>
    {/* Centered form */}
    <div className="relative z-10 w-full max-w-[600px] overflow-hidden rounded-lg bg-black/50 p-6 shadow-lg">
      {children}
    </div>
  </div>
);

// Default layout (fallback)
const DefaultLayout: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => (
  <div className="flex h-screen items-start justify-center overflow-hidden p-4">
    <div className="w-full max-w-[550px] p-4">{children}</div>
  </div>
);

// Map prompt codes to layout components
export const LayoutConfig: Record<
  string,
  React.FC<{ children: React.ReactNode }>
> = {
  'half-image': HalfImageHalfFormLayout,
  'full-form': FullFormLayout,
  'background-image': CenteredFormWithBackgroundLayout,
  default: DefaultLayout,
};
