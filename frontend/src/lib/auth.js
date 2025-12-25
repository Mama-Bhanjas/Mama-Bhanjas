import crypto from 'crypto';

// Use a simple secret from env or fallback
const JWT_SECRET = process.env.JWT_SECRET || 'your-default-secret-change-this';

/**
 * Hash a password using Node's built-in crypto module (PBKDF2)
 */
export function hashPassword(password) {
    const salt = crypto.randomBytes(16).toString('hex');
    const hash = crypto.pbkdf2Sync(password, salt, 1000, 64, 'sha512').toString('hex');
    return `${salt}:${hash}`;
}

/**
 * Verify a password against a hash
 */
export function verifyPassword(password, storedHash) {
    const [salt, hash] = storedHash.split(':');
    const verifyHash = crypto.pbkdf2Sync(password, salt, 1000, 64, 'sha512').toString('hex');
    return hash === verifyHash;
}

/**
 * Simple manual JWT-like token generation (Signed JSON)
 * Using standard base64url encoding
 */
export function signToken(payload) {
    const header = Buffer.from(JSON.stringify({ alg: 'HS256', typ: 'JWT' })).toString('base64url');
    const data = Buffer.from(JSON.stringify({ ...payload, exp: Date.now() + 3600000 })).toString('base64url');

    const signature = crypto
        .createHmac('sha256', JWT_SECRET)
        .update(`${header}.${data}`)
        .digest('base64url');

    return `${header}.${data}.${signature}`;
}

/**
 * Verify manual JWT
 */
export function verifyToken(token) {
    try {
        const [header, data, signature] = token.split('.');
        const verifySignature = crypto
            .createHmac('sha256', JWT_SECRET)
            .update(`${header}.${data}`)
            .digest('base64url');

        if (signature !== verifySignature) return null;

        const payload = JSON.parse(Buffer.from(data, 'base64url').toString());
        if (payload.exp < Date.now()) return null;

        return payload;
    } catch (e) {
        return null;
    }
}
