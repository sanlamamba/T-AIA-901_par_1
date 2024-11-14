import { SignIn } from "@clerk/nextjs";

export default function SignedInPage(){
    return (
        <div className="flex justify-center items-center h-full">
            <SignIn />
        </div>
    )
}