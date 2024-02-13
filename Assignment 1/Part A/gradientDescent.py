def Sonar(x, y, initialGuess):
    thetha1 = [initialGuess[0]] * 1000000
    thetha2 = [initialGuess[1]] * 1000000
    thetha = [0] * 2
    J2 = [0] * 10
    J1 = [0] * 10

    sigma = 1e-7
    alpha = 0.1                
    
    for ii in range(0,1000000-1):
        for nn in range(0,10):
            J1[nn] = -2*(y[nn] - thetha1[ii] - thetha2[ii]*x[nn]);
            J2[nn] = -2*x[nn]*(y[nn] - thetha1[ii] - thetha2[ii]*x[nn]); 
            
        thetha1[ii+1] = thetha1[ii] - alpha*sum(J1);
        thetha2[ii+1] = thetha2[ii] - alpha*sum(J2);        
        
        if ((thetha1[ii+1] - thetha1[ii] < sigma) & (thetha2[ii+1] - thetha2[ii] < sigma)):
            break
                
    thetha[0] = thetha1[ii+1]
    thetha[1] = thetha2[ii+1]
     
    return thetha   

def IR(x, y, initialGuess):
    thetha1 = [initialGuess[0]] * 1000000
    thetha2 = [initialGuess[1]] * 1000000
    thetha3 = [initialGuess[2]] * 1000000
    
    thetha = [0] * 3
    J2 = [0] * 10
    J1 = [0] * 10
    J3 = [0] * 10
    
    sigma = 1e-7
    alpha = 1e-6
    
    for ii in range(0,1000000-1):
        for nn in range(0,10):
            J1[nn] = -2*(y[nn] - thetha1[ii] - thetha2[ii]*(1/x[nn]) - thetha3[ii]*x[nn]);
            J2[nn] = (-2/x[nn])*(y[nn] - thetha1[ii] - thetha2[ii]*(1/x[nn])- thetha3[ii]*x[nn]);   
            J3[nn] = -2*x[nn]*(y[nn] - thetha1[ii] - thetha2[ii]*(1/x[nn]) - thetha3[ii]*x[nn]); 

            
        thetha1[ii+1] = thetha1[ii] - alpha*sum(J1);
        thetha2[ii+1] = thetha2[ii] - alpha*sum(J2);        
        thetha3[ii+1] = thetha3[ii] - alpha*sum(J3);        
        
        
        if ((thetha1[ii+1] - thetha1[ii] < sigma) & (thetha2[ii+1] - thetha2[ii] < sigma) & (thetha3[ii+1] - thetha3[ii] < sigma)):
            break
                
    thetha[0] = thetha1[ii+1]
    thetha[1] = thetha2[ii+1]
    thetha[2] = thetha3[ii+1]
    
    return thetha   