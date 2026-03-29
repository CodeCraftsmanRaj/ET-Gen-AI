import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { telegramId, email, name, phone } = body

    if (!telegramId && !email) {
      return NextResponse.json(
        { error: 'Please provide either telegramId or email' },
        { status: 400 }
      )
    }

    // Check if user already exists
    if (telegramId) {
      const existing = await prisma.user.findUnique({ where: { telegramId } })
      if (existing) {
        return NextResponse.json({ user: existing, message: 'User already exists' })
      }
    }
    if (email) {
      const existing = await prisma.user.findUnique({ where: { email } })
      if (existing) {
        return NextResponse.json({ user: existing, message: 'User already exists' })
      }
    }

    const user = await prisma.user.create({
      data: {
        telegramId: telegramId || null,
        email: email || null,
        name: name || null,
        phone: phone || null,
      },
    })

    return NextResponse.json({ user }, { status: 201 })
  } catch (error: any) {
    console.error('Signup error:', error)
    return NextResponse.json(
      { error: 'Signup failed: ' + error.message },
      { status: 500 }
    )
  }
}
