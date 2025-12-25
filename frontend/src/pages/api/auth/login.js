import { getDb } from '../../../lib/db';
import { verifyPassword, signToken } from '../../../lib/auth';

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ message: 'Method not allowed' });
    }

    const { email, password } = req.body;

    if (!email || !password) {
        return res.status(400).json({ message: 'Email and password are required' });
    }

    try {
        const db = await getDb();
        const user = await db.get('SELECT * FROM users WHERE email = ?', [email]);

        if (!user || !verifyPassword(password, user.password)) {
            return res.status(401).json({ message: 'Invalid credentials' });
        }

        const token = signToken({ sub: user.email, name: user.full_name });

        return res.status(200).json({
            access_token: token,
            token_type: 'bearer',
            user: {
                id: user.id,
                email: user.email,
                full_name: user.full_name,
                avatar_url: user.avatar_url
            }
        });
    } catch (error) {
        console.error('Login Error:', error);
        return res.status(500).json({ message: 'Internal server error' });
    }
}
