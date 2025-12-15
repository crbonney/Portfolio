function ModelRobot (theta1, theta2)


    f1 = TransformPoints(TRANS0_1(theta1),frame1_links);
    f2 = TransformPoints(TRANS0_1(theta1),TransformPoints(TRANS1_2(theta2),frame2_links));


%     plot3(frame0_links(1,:),frame0_links(2,:), frame0_links(3,:),'bs-','LineWidth',3);
    axis([-15 15 -15 15 -15 15]);
    grid on
    hold on
    xlabel('x');
    ylabel('y');
    zlabel('z');
%     plot3(f1(1,:),f1(2,:), f1(3,:),'rs-','LineWidth',3);
    plot3(f2(1,:),f2(2,:), f2(3,:),'go-', 'MarkerFaceColor', 'c', 'MarkerSize',5,'LineWidth',3);
    axis([-15 15 -15 15 -15 15]);
%     WorkEnvelope2(rho, phi_max);
    hold off

end

