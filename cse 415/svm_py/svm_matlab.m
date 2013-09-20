clear;
clc;
X =load('data.txt');
n = length(X);  %length of data.
y = X(:,4); %target class label vector.
X = X(:,1:3);   %example vector.
TOL = 0.0001;   %tolerance.
C = 1;  %constant, weight for loss function. KKT boundary.
b = 0;  
Wold = 0;   %W is the objective function
Wnew = 0;   
for i = 1 : 50 %set the class label to 1 or -1
    y(i) = -1;
end
a = zeros(n,1); %alpha's
for i = 1 : n	%set class label to 1 or -1.
        a(i) = 0.2;
end

%Storing a Kernel matrix lookup table for fast future access.
K = ones(n,n);
for i = 1 :n
    for j = 1 : n
        K(i,j) = k(X(i,:),X(j,:));
    end
end
sum = zeros(n,1);% sum(k)=sigma a(i)*y(i)*K(k,i);
for k = 1 : n
    for i = 1 : n
        sum(k) = sum(k) + a(i) * y(i) * K(i,k);
    end
end

while 1	%selections

    n1 = 1;	%indices for the two locations.
    n2 = 2;
    %n1 is chosen to be the first to violate the KKT condition.
    while n1 <= n
        if y(n1) * (sum(n1) + b) == 1 && a(n1) >= C && a(n1) <=  0
             break;
        end
        if y(n1) * (sum(n1) + b) > 1 && a(n1) ~=  0
               break;
        end
        if y(n1) * (sum(n1) + b) < 1 && a(n1) ~=C
              break;
        end
         n1 = n1 + 1;              
    end
    %n2 is chosen by having the maximum |E1 - E2|
    E1 = 0;
    E2 = 0;
    maxDiff = 0;	%the max error of the assumption.
    E1 = sum(n1) + b - y(n1);	%Error of choosing n1.
    for i = 1 : n
        tempSum = sum(i) + b - y(i);
        if abs(E1 - tempSum)> maxDiff
            maxDiff = abs(E1 - tempSum);
            n2 = i;
            E2 = tempSum;
        end
    end

    %updates
    a1old = a(n1);
    a2old = a(n2);
    KK = K(n1,n1) + K(n2,n2) - 2*K(n1,n2);
    a2new = a2old + y(n2) *(E1 - E2) / KK;	%calculate new a2
    %a2 must satisfy the constraints.
    S = y(n1) * y(n2);
    if S == -1
        L = max(0,a2old - a1old);
        H = min(C,C - a1old + a2old);
    else
        L = max(0,a1old + a2old - C);
        H = min(C,a1old + a2old);
    end
    if a2new > H
        a2new = H;
    end
    if a2new < L
        a2new = L;
    end
    a1new = a1old + S * (a2old - a2new);	%calculate new a1
    a(n1) = a1new;	%updating a
    a(n2) = a2new;

    %some updates
    sum = zeros(n,1);	%sum(k)=sigma a(i)*y(i)*K(k,i);
    for k = 1 : n
        for i = 1 : n
            sum(k) = sum(k) + a(i) * y(i) * K(i,k);
        end
    end
    Wold = Wnew;
    Wnew = 0;	%W(a) after updating a.
				%W(a) = sigma a(i) - 0.5 * sigma sigma y(i)*y(j)*k(i,j)*a(i)*a(j)
    tempSum = 0;	
    for i = 1 : n
        for j = 1 : n
        tempSum= tempSum + y(i)*y(j)*a(i)*a(j)*K(i,j);
        end
        Wnew= Wnew+ a(i);
    end
    Wnew= Wnew - 0.5 * tempSum;
    %the following updates b: through finding a support vector.
    support = 1;	%initialize support vector.
    while abs(a(support))< 1e-4 && support <= n
        support = support + 1;
    end
    b = 1 / y(support) - sum(support);
    %loop exit condition. 
    if abs(Wnew/ Wold - 1 ) <= TOL
        break;
    end
end
%result: original classification, 
for i = 1 : n
    fprintf('point %d:original label ',i);
    if i <= 50
        fprintf('-1');
    else
        fprintf(' 1');
    end
    fprintf('    classification function value%f      classification result:',sum(i) + b);
    if abs(sum(i) + b - 1) < 0.5
        fprintf('1\n');
    else if abs(sum(i) + b + 1) < 0.5
            fprintf('-1\n');
        else
            fprintf('classification error\n');
        end
    end
end
