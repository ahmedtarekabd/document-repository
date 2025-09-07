'use client'

import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import useSession from '@/hooks/useSession'
import { FileText, Search, Upload, Users } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function HomePage() {
  const { user, status } = useSession()

  if (status === 'loading') {
    return (
      <div className='flex min-h-screen items-center justify-center'>
        <div className='border-primary h-8 w-8 animate-spin rounded-full border-b-2'></div>
      </div>
    )
  }

  if (!user) {
    return (
      <div className='from-background to-muted/20 min-h-screen bg-gradient-to-br'>
        <div className='container mx-auto px-4 py-16'>
          <div className='mb-16 text-center'>
            <h1 className='mb-4 text-4xl font-bold tracking-tight'>
              Document Repository
            </h1>
            <p className='text-muted-foreground mx-auto mb-8 max-w-2xl text-xl'>
              Secure document management with advanced search, version control,
              and role-based access
            </p>
            <div className='flex justify-center gap-4'>
              <Button asChild size='lg'>
                <Link to='/auth/login'>Sign In</Link>
              </Button>
              <Button asChild variant='outline' size='lg'>
                <Link to='/auth/signup'>Sign Up</Link>
              </Button>
            </div>
          </div>

          <div className='mx-auto grid max-w-6xl gap-6 md:grid-cols-2 lg:grid-cols-4'>
            <Card>
              <CardHeader>
                <FileText className='text-primary mb-2 h-8 w-8' />
                <CardTitle>Document Management</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Upload, organize, and manage documents with metadata and
                  tagging
                </CardDescription>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <Search className='text-primary mb-2 h-8 w-8' />
                <CardTitle>Advanced Search</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Search by title, tags, and filter by access roles with
                  pagination
                </CardDescription>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <Upload className='text-primary mb-2 h-8 w-8' />
                <CardTitle>Version Control</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Track document versions and maintain complete history
                </CardDescription>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <Users className='text-primary mb-2 h-8 w-8' />
                <CardTitle>Role-based Access</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Control access with admin, editor, and viewer permissions
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className='bg-background min-h-screen'>
      <div className='container mx-auto px-4 py-8'>
        <div className='mb-8 flex items-center justify-between'>
          <div>
            <h1 className='text-3xl font-bold'>Welcome back, {user.name}</h1>
            <p className='text-muted-foreground'>
              Manage your documents and search the repository
            </p>
          </div>
          <div className='flex gap-4'>
            <Button asChild>
              <Link to='/upload'>
                <Upload className='mr-2 h-4 w-4' />
                Upload Document
              </Link>
            </Button>
            <Button asChild variant='outline'>
              <Link to='/search'>
                <Search className='mr-2 h-4 w-4' />
                Search Documents
              </Link>
            </Button>
          </div>
        </div>

        <div className='grid gap-6 md:grid-cols-3'>
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className='space-y-2'>
              <Button asChild variant='ghost' className='w-full justify-start'>
                <Link to='/upload'>
                  <Upload className='mr-2 h-4 w-4' />
                  Upload New Document
                </Link>
              </Button>
              <Button asChild variant='ghost' className='w-full justify-start'>
                <Link to='/search'>
                  <Search className='mr-2 h-4 w-4' />
                  Search Repository
                </Link>
              </Button>
              <Button asChild variant='ghost' className='w-full justify-start'>
                <Link to='/documents/my'>
                  <FileText className='mr-2 h-4 w-4' />
                  My Documents
                </Link>
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
            </CardHeader>
            <CardContent>
              <p className='text-muted-foreground text-sm'>
                Recent document activity will appear here
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Statistics</CardTitle>
            </CardHeader>
            <CardContent>
              <p className='text-muted-foreground text-sm'>
                Document statistics and insights will appear here
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
