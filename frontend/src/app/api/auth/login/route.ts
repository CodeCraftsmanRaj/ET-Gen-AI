import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { telegramId, email } = body

    if (!telegramId && !email) {
      return NextResponse.json(
        { error: 'Please provide either telegramId or email' },
        { status: 400 }
      )
    }

    let user = null
    if (telegramId) {
      user = await prisma.user.findUnique({ where: { telegramId } })
    } else if (email) {
      user = await prisma.user.findUnique({ where: { email } })
    }

    if (!user) {
      return NextResponse.json(
        { error: 'User not found. Please sign up first.' },
        { status: 404 }
      )
    }

    return NextResponse.json({ user })
  } catch (error: any) {
    console.error('Login error:', error)
    return NextResponse.json(
      { error: 'Login failed: ' + error.message },
      { status: 500 }
    )
  }
}
