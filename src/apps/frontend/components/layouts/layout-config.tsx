import React from 'react';

// Layout 1: Half image and half form
const HalfImageHalfFormLayout: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => (
  <div className="flex h-screen flex-col md:flex-row">
    {/* Image Section (Top on Mobile, Left on Desktop) */}
    <div
      className="h-1/3 bg-cover bg-center md:h-auto md:w-1/2"
      style={{ backgroundImage: 'url(/assets/img/auth-background.jpg)' }}
    />
    {/* Form Section (Bottom on Mobile, Right on Desktop) */}
    <div className="flex h-2/3 w-full items-center justify-center p-4 md:h-auto md:w-1/2">
      <div className="w-full max-w-md rounded-lg bg-white p-6 shadow-md sm:max-w-lg md:max-w-xl">
        {children}
      </div>
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
    <div className="absolute inset-0 bg-black/40"></div>
    {/* Centered form */}
    <div className="relative z-10 w-full max-w-md rounded-lg bg-black/40 p-6 shadow-lg sm:max-w-lg md:max-w-xl">
      {children}
    </div>
  </div>
);

// Default layout (fallback)
const DefaultLayout: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => (
  <div className="flex items-start justify-center overflow-hidden p-4">
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
