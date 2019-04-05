class AccessController < ApplicationController

  # user cannot access profile page unless logged in
  before_action :confirm_logged_in, :except => [:login, :attempt_login, :logout, :signup, :attempt_signup]

  # navigates to users profile page
  # checks if user is banned or not
  # if banned or recently unbanned after 7 days, user is notified
  def index
    @user = User.find(session[:user_id])
    @banned = false
    if @user.ban_date != nil
      if Date.today - 7.days > @user.ban_date
        @user.ban_date = nil
        @user.reported = 0
        @user.save
        flash[:notice] = "Unbanned"
      else
        @banned = true
        flash[:notice] = "BANNED"
      end
    end
    @myopendebates = OpenDebate.where(user_id: @user.id).sorted
    @mybinarydebates = BinaryDebate.where(user_id: @user.id).sorted
  end

  # navigates to login page
  def login
  end

  # checks if user has entered correct credentials to log in
  # username and password must be present
  # username must exist
  # hashed password generated from password input must match password digest of that user
  # if correct - user logged in, session key stored, redirected to user profile page
  def attempt_login
    if params[:username].present? && params[:password].present?
      located = User.where(:username => params[:username]).first
      if located
        authorized = located.authenticate(params[:password])
      end
    end
    if authorized
      session[:user_id] = authorized.id
      session[:username] = authorized.username
      redirect_to(:action => 'index')
    else
      redirect_to(:action => 'login')
      flash[:notice] = "Incorrect username or password"
    end
  end

  # removes session, logs user out, redirects to login page
  def logout
    session[:user_id] = nil
    session[:username] = nil
    redirect_to(:action => "login")
    flash[:notice] = "You logged out"
  end

  # navigates to sign up page
  def signup
  end

  # checks if user has entered correct credentials to log in
  # username, email, password and confirm password must be present
  # username must not already exist
  # email should match email regex
  # passwords should match
  # passwords should match password regex
  # if correct - user signed up, user logged in, session key stored, redirected to user profile page
  def attempt_signup
    if params[:username].present? && params[:password].present? &&
      params[:email].present? && params[:password_confirm].present?
      if params[:password] == params[:password_confirm]
        @new_user = User.new(:email => params[:email], :username => params[:username])
        @new_user.password = params[:password]
        if @new_user.save
          redirect_to(:action => "attempt_login", :username => params[:username], :password => params[:password])
        else
          redirect_to(:action => "signup")
          flash[:notice] = "The password entered is not strong enough"
        end
      else
        redirect_to(:action => "signup")
        flash[:notice] = "Passwords do not match"
      end
    else
      redirect_to(:action => "signup")
      flash[:notice] = "Please fill out all information"
    end
  end

end
