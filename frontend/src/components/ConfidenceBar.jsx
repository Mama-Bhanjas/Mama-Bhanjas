import React from 'react';

export default function ConfidenceBar({ confidence }) {
    // confidence is a number between 0 and 100
    return (
        <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div
                className="bg-blue-600 h-2.5 rounded-full"
                style={{ width: `${confidence}%` }}
            ></div>
        </div>
    );
}
