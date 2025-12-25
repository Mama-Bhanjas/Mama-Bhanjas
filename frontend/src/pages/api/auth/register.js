import { getDb } from '../../../lib/db';
import { hashPassword } from '../../../lib/auth';

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ message: 'Method not allowed' });
    }

    const { full_name, email, password } = req.body;

    if (!email || !password) {
        return res.status(400).json({ message: 'Email and password are required' });
    }

    try {
        const db = await getDb();

        // Check if user already exists
        const existingUser = await db.get('SELECT * FROM users WHERE email = ?', [email]);
        if (existingUser) {
            return res.status(400).json({ message: 'User already exists' });
        }

        const hashedPassword = hashPassword(password);
        const userId = Math.random().toString(36).substr(2, 9);
        const avatarUrl = `https://api.dicebear.com/7.x/avataaars/svg?seed=${email}`;

        await db.run(
            'INSERT INTO users (id, full_name, email, password, avatar_url) VALUES (?, ?, ?, ?, ?)',
            [userId, full_name, email, hashedPassword, avatarUrl]
        );

        return res.status(201).json({
            id: userId,
            full_name,
            email,
            avatar_url: avatarUrl
        });
    } catch (error) {
        console.error('Registration Error:', error);
        return res.status(500).json({ message: 'Internal server error' });
    }
}
