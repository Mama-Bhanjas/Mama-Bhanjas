import React from 'react';

export default function SourceBadge({ verified, reputation }) {
    return (
        <div className="flex items-center space-x-1">
            {verified && (
                <span className="bg-green-100 text-green-800 text-xs font-semibold px-2 py-0.5 rounded">
                    Verified
                </span>
            )}
            {reputation && (
                <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-2 py-0.5 rounded">
                    Rep: {reputation}
                </span>
            )}
        </div>
    );
}
