import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import crypto from 'crypto'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { email, name, phone } = body

    if (!email) {
      return NextResponse.json(
        { error: 'Email is required' },
        { status: 400 }
      )
    }

    // Basic email validation
    if (!email.includes('@')) {
      return NextResponse.json(
        { error: 'Invalid email format' },
        { status: 400 }
      )
    }

    // Check if user already exists
    const existing = await prisma.user.findUnique({ where: { email } })
    if (existing) {
      return NextResponse.json(
        { user: existing, message: 'User already exists. Use login instead.' },
        { status: 409 }
      )
    }

    // Generate a simple auth token
    const authToken = crypto.randomBytes(32).toString('hex')

    // Create new user
    const user = await prisma.user.create({
      data: {
        email: email.toLowerCase(),
        name: name || 'User',
        phone: phone || null,
        authToken: authToken,
      },
    })

    return NextResponse.json(
      { 
        user: {
          id: user.id,
          email: user.email,
          name: user.name,
          phone: user.phone,
          authToken: user.authToken,
        },
        message: 'Signup successful'
      },
      { status: 201 }
    )
  } catch (error: any) {
    console.error('Signup error:', error)
    return NextResponse.json(
      { error: 'Signup failed: ' + error.message },
      { status: 500 }
    )
  }
}
