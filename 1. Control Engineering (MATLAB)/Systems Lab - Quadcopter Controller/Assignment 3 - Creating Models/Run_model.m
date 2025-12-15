function Run_model(input,states,outputs)

output = sim('Drone_Model', 0:0.001:6);

linear = output.linear.Data;
nonlinear = output.nonlinear.Data;
linear_states = (output.linearstates.Data)';
nonlinear_states = squeeze(output.nonlinearstates.Data);
time = output.linear.Time;

n_states = nnz(states);
if (n_states == 1)
    subplot_size = [2,1];
elseif (n_states == 2)
    subplot_size = [2,2];
else 
    subplot_size = [2,4];
end

nonlinear_graph = figure('Color', 'w');
sgtitle(['System States, Input: ' input]);
plot_num = 1;
for i=1:4
    if (states(i))
        switch i            
            case 1
                subplot(subplot_size(1),subplot_size(2),plot_num);
                plot(time,nonlinear_states(1:3,:));
                title('Nonlinear Position States');
                legend({'X_{NED}','Y_{NED}','Z_{NED}'},'Location','Best');
                ylabel('position (m)');
                xlabel('time (s)');

                plot_num = plot_num + 1;

                subplot(subplot_size(1),subplot_size(2),plot_num);
                plot(time,linear_states(1:3,:));
                title('Linear Position States');
                legend({'X_{NED}','Y_{NED}','Z_{NED}'},'Location','Best');
                ylabel('position (m)');
                xlabel('time (s)');

                plot_num = plot_num + 1;
            case 2
                subplot(subplot_size(1),subplot_size(2),plot_num);
                plot(time,nonlinear_states(4:6,:));
                title('Nonlinear Velocity States');
                legend({'u','v','w'},'Location','Best');
                ylabel('velocity (m/s)');
                xlabel('time (s)');

                plot_num = plot_num + 1;     
                
                subplot(subplot_size(1),subplot_size(2),plot_num);
                plot(time,linear_states(4:6,:));
                title('Linear Velocity States');
                legend({'u','v','w'},'Location','Best');
                ylabel('velocity (m/s)');
                xlabel('time (s)');

                plot_num = plot_num + 1;
            case 3
                subplot(subplot_size(1),subplot_size(2),plot_num);
                plot(time,nonlinear_states(7:9,:));
                title('Nonlinear UAV Euler Angles');
                legend({'\phi','\theta','\psi'},'Location','Best');
                ylabel('angle (rad)');
                xlabel('time (s)');
           
                plot_num = plot_num + 1;   
                
                subplot(subplot_size(1),subplot_size(2),plot_num);
                plot(time,linear_states(7:9,:));
                title('Linear Euler Angle States');
                legend({'\phi','\theta','\psi'},'Location','Best');
                ylabel('angle (rad)');
                xlabel('time (s)');
           
                plot_num = plot_num + 1;               
            case 4
                subplot(subplot_size(1),subplot_size(2),plot_num);
                plot(time,nonlinear_states(10:12,:));
                title('Nonlinear Angular Velocity States');
                legend({'p','q','r'},'Location','Best');
                ylabel('angular velocity (rad/s)');
                xlabel('time (s)');

                plot_num = plot_num + 1;        
                
                subplot(subplot_size(1),subplot_size(2),plot_num);
                plot(time,linear_states(10:12,:));
                title('Linear Angular Velocity States');
                legend({'p','q','r'},'Location','Best');
                ylabel('angular velocity (rad/s)');
                xlabel('time (s)');

                plot_num = plot_num + 1;               
        end 
    end  
end


n_states = nnz(outputs);
if (n_states == 1)
    subplot_size = [1,1];
elseif (n_states == 2)
    subplot_size = [1,2];
else 
    subplot_size = [2,2];
end

output_graph = figure('Color', 'w');
sgtitle(['Outputs, Input: ' input]);

plot_num = 1;
for i=1:4
    if (outputs(i))
        switch i            
            case 1
                subplot(subplot_size(1),subplot_size(2),plot_num);
                plot(time,linear(:,1))
                hold on
                plot(time,nonlinear(:,1))
                title('UAV height')
                legend({'linear', 'nonlinear'},'Location','Best');
                ylabel('position (m)');
                xlabel('time (s)');

                plot_num = plot_num + 1;                
            case 2
                subplot(subplot_size(1),subplot_size(2),plot_num);
                plot(time,linear(:,2))
                hold on
                plot(time,nonlinear(:,2))
                title('acceleration in x')
                legend({'linear', 'nonlinear'},'Location','Best');
                ylabel('acceleration (m/s2)');
                xlabel('time (s)');

                plot_num = plot_num + 1;                
            case 3
                subplot(subplot_size(1),subplot_size(2),plot_num);
                plot(time,linear(:,3))
                hold on
                plot(time,nonlinear(:,3))
                title('acceleration in y')
                legend({'linear', 'nonlinear'},'Location','Best');
                ylabel('acceleration (m/s2)');
                xlabel('time (s)');
           
                plot_num = plot_num + 1;               
            case 4
                subplot(subplot_size(1),subplot_size(2),plot_num);
                plot(time,linear(:,4));
                hold on
                plot(time,nonlinear(:,4)+9.81);
                title('acceleration in z')
                legend({'linear', 'nonlinear'},'Location','Best');
                ylabel('acceleration (m/s2)');
                xlabel('time (s)');

                plot_num = plot_num + 1;               
        end 
    end  
end


end

