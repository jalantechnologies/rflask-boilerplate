import clsx from 'clsx';
import * as React from 'react';

interface TagProps extends React.InputHTMLAttributes<HTMLInputElement> {
    startEnhancer?: React.ReactElement | string;
    text?: string;
    textAlign?: 'left' | 'center' | 'right';
    colorVal?: string;  // Renamed to camelCase for consistency
}

const Tag: React.FC<TagProps> = ({
    startEnhancer,
    text,
    textAlign = 'left',
    colorVal = 'gray',
}) => (
    <div
        className={clsx([
            'inline-flex items-center rounded-lg px-2 py-1 m-1', 
        ])}
        style={{ backgroundColor: colorVal }} 
    >
        {startEnhancer && (
            <span className="flex items-center justify-center mr-2">
                {startEnhancer}
            </span>
        )}
        <label
            className="text-xs lg:text-sm" 
            style={{
                textAlign: textAlign,
                color: 'black',
            }}
        >
            {text}
        </label>
    </div>
);

export default Tag;
