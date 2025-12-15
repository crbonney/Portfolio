
input_file = fopen("input.txt", "r");

regex = "\\d+";
tol = 10^(-2);

A_data = 0;
token_sum = 0;
while true
  A_data = fgetl(input_file);
  if A_data == -1
    break
  endif
  [~,~,~,A_match,~,~,~] = regexp(A_data,regex);
  B_data = fgetl(input_file);
  [~,~,~,B_match,~,~,~] = regexp(B_data,regex);
  goal   = fgetl(input_file);
  [~,~,~,goal_match,~,~,~] = regexp(goal,regex);
  fgetl(input_file);
  
  A_x = str2double(cell2mat(A_match(1,1)));
  A_y = str2double(cell2mat(A_match(1,2)));
  B_x = str2double(cell2mat(B_match(1,1)));
  B_y = str2double(cell2mat(B_match(1,2)));

  goal_x = str2double(cell2mat(goal_match(1,1)));
  goal_y = str2double(cell2mat(goal_match(1,2)));

  goal_x += 10000000000000;
  goal_y += 10000000000000;
        
  detA = A_x*B_y - A_y*B_x;
  detA1 = goal_x*B_y - goal_y*B_x;
  detA2 = A_x*goal_y - A_y*goal_x;

  rref_res = rref([A,b]);
  
  result = [detA1/detA ; detA2/detA];
  
  
  if mod(detA1, detA) == 0 && mod(detA2,detA) == 0
    token_sum += 3*result(1) + result(2);
##    disp("valid")
    endif

end

printf("token total = %.*f", 1 ,token_sum)