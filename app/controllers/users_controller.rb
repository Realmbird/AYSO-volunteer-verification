class UsersController < ApplicationController
    before_action :search, only: :index
    def search
        @players = Player.first(100)
    end

    def index
        @users = User.all
    end
    def show
        @user = current_user
    end
    def edit
        @user = current_user
    end
end
