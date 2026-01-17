Deployment of Java Application:
Lets get the sample code from the Code repository to the local Linux terminal.
Sample Code Link:  https://github.com/harish628/one-devops.git
Command: git clone https://github.com/harish628/one-devops.git and get into the Directory, then switch to master.

<img width="887" height="271" alt="image" src="https://github.com/user-attachments/assets/968c9e53-c36b-4780-887c-f38ce2d7dda2" />


Install maven on your system to build the WAR file using below command.
Command: yum install maven -y
<img width="940" height="185" alt="image" src="https://github.com/user-attachments/assets/12aedfdb-50b1-4b41-8753-1cc158022fe7" />

 
Run the maven to create the war file
Command: mvn clean package
<img width="799" height="167" alt="image" src="https://github.com/user-attachments/assets/354436a7-42b8-40e2-8df2-a04c00cca5e9" />


After Completion you will be able to see the updated build status info as below
<img width="940" height="260" alt="image" src="https://github.com/user-attachments/assets/fb432be9-d9e5-492f-90b9-6164f717f751" />

 
Once build successful create the image and container.
<img width="924" height="231" alt="image" src="https://github.com/user-attachments/assets/bef0dcf4-a51a-47a5-9d3d-9c450c03666e" />

 <img width="940" height="89" alt="image" src="https://github.com/user-attachments/assets/a4a5c563-9a64-4ee5-b46f-0344689c6105" />

You will be able to see the Application is properly got deployed on the Tomcat server.
 
 <img width="940" height="528" alt="image" src="https://github.com/user-attachments/assets/aa507a23-5ced-4686-a13d-efffd70be35b" />

Access myapp and you will be able to see your application.

<img width="940" height="528" alt="image" src="https://github.com/user-attachments/assets/699fca42-f680-4c41-b57e-ad0683c9ec53" />
