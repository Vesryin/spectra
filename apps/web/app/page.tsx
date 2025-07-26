'use client';

import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Brain, MessageCircle, Heart, Database } from 'lucide-react';
import Link from 'next/link';

export default function HomePage() {
  return (
    <div className='min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50'>
      {/* Hero Section */}
      <section className='relative py-24 px-4 sm:px-6 lg:px-8'>
        <div className='mx-auto max-w-4xl text-center'>
          <div className='mb-8 flex justify-center'>
            <div className='rounded-full bg-gradient-to-r from-blue-600 to-purple-600 p-4'>
              <Brain className='h-12 w-12 text-white' />
            </div>
          </div>

          <h1 className='mb-6 text-5xl font-bold tracking-tight text-gray-900 sm:text-6xl'>
            Meet{' '}
            <span className='bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent'>
              SpectraAI
            </span>
          </h1>

          <p className='mx-auto mb-8 max-w-2xl text-xl leading-8 text-gray-600'>
            The next generation of AI assistants with advanced memory, emotional
            intelligence, and adaptive personality. Built for meaningful
            conversations that evolve.
          </p>

          <div className='flex flex-col gap-4 sm:flex-row sm:justify-center'>
            <Button
              asChild
              size='lg'
              className='bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700'
            >
              <Link href='/chat'>
                <MessageCircle className='mr-2 h-5 w-5' />
                Start Chatting
              </Link>
            </Button>
            <Button asChild variant='outline' size='lg'>
              <Link href='/dashboard'>View Dashboard</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className='py-16 px-4 sm:px-6 lg:px-8'>
        <div className='mx-auto max-w-6xl'>
          <div className='mb-12 text-center'>
            <h2 className='mb-4 text-3xl font-bold text-gray-900'>
              Advanced AI Capabilities
            </h2>
            <p className='text-lg text-gray-600'>
              SpectraAI combines cutting-edge technology with intuitive design
            </p>
          </div>

          <div className='grid gap-8 md:grid-cols-2 lg:grid-cols-4'>
            {features.map((feature, index) => (
              <Card
                key={index}
                className='border-0 bg-white/70 backdrop-blur-sm transition-all hover:bg-white/80 hover:shadow-lg'
              >
                <CardHeader>
                  <div className='mb-2 flex h-12 w-12 items-center justify-center rounded-lg bg-gradient-to-r from-blue-600 to-purple-600'>
                    <feature.icon className='h-6 w-6 text-white' />
                  </div>
                  <CardTitle className='text-xl'>{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className='text-gray-600'>
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className='bg-white/30 py-16 px-4 backdrop-blur-sm sm:px-6 lg:px-8'>
        <div className='mx-auto max-w-4xl'>
          <div className='grid gap-8 text-center md:grid-cols-3'>
            <div>
              <div className='mb-2 text-4xl font-bold text-gray-900'>7B</div>
              <div className='text-gray-600'>Parameters in AI Model</div>
            </div>
            <div>
              <div className='mb-2 text-4xl font-bold text-gray-900'>∞</div>
              <div className='text-gray-600'>Memory Capacity</div>
            </div>
            <div>
              <div className='mb-2 text-4xl font-bold text-gray-900'>2025</div>
              <div className='text-gray-600'>Modern Tech Stack</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

const features = [
  {
    icon: Brain,
    title: 'Advanced AI Brain',
    description:
      'Powered by OpenHermes-2.5-Mistral-7B for intelligent conversations',
  },
  {
    icon: Heart,
    title: 'Emotional Intelligence',
    description: 'Real-time emotion processing and empathetic responses',
  },
  {
    icon: Database,
    title: 'Persistent Memory',
    description: 'Remembers context and builds lasting relationships',
  },
  {
    icon: MessageCircle,
    title: 'Real-time Chat',
    description: 'Lightning-fast responses with WebSocket connectivity',
  },
];
