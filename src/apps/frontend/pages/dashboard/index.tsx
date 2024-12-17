import * as React from 'react';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';
import AuthenticationPageLayout from '../authentication/authentication-page-layout';
import AuthenticationFormLayout from '../authentication/authentication-form-layout';
import { Button, H2, VerticalStackLayout } from '../../components';
import routes from '../../constants/routes';
const Dashboard: React.FC = () => {
    const navigate = useNavigate();
    const onSuccess = () => {
        toast.success(
            'Your account has been successfully created. Please login to continue.',
        );
        navigate(routes.ADDTASK);
    };
    return (
        <AuthenticationPageLayout>
            <AuthenticationFormLayout>
                <VerticalStackLayout gap={1}>
                    <H2>Today</H2>
                    <Button onClick={() => onSuccess()}>Add Tasks</Button>
                </VerticalStackLayout>
            </AuthenticationFormLayout>
        </AuthenticationPageLayout>
    )
};

export default Dashboard;
