import SignUpForm from '@/components/SignUpForm'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import useSession from '@/hooks/useSession'
import { useNavigate } from 'react-router-dom'

const SignUp = () => {
  const session = useSession()
  const navigate = useNavigate()
  if (session.status === 'authenticated') {
    navigate('/')
    return
  }
  return (
    <div className='flex h-screen items-center justify-center'>
      <Card className='w-full max-w-sm shadow-md'>
        <CardHeader className='space-y-4'>
          <CardTitle className='text-lg font-bold'>Sign-up</CardTitle>
          <CardDescription>
            Sign-up to Document Repository to start coding with your friends in
            real-time.
          </CardDescription>
        </CardHeader>
        <CardContent className='w-full'>
          <SignUpForm />
        </CardContent>
      </Card>
    </div>
  )
}

export default SignUp
