class UsersController < ApplicationController
    before_action :search, only: :index
    def search
        @players = Player.all

        search_params.each do |key, value|
            @players = @players.where("#{key} LIKE ?", "%#{value}%") if value.present?
        end

        @players = @players.limit(100)
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

    private

    def search_params
        params.permit(:search_term, :program_name, :division_name, :team_name, :order_payment_status, :postal_code, :city, :state)
    end
end
