class VolunteersController < ApplicationController
    before_action :search, only: :index
    def search
        @volunteers = Volunteer.all

        search_params.each do |key, value|
            @volunteers = @volunteers.where("#{key} LIKE ?", "%#{value}%") if value.present?
        end

        @volunteers = @volunteers.limit(100)
    end

    def index
        @volunteers = search
    end

    def show
        @volunteer = Volunteer.find(params[:id])
    end

    def edit
        @volunteer = Volunteer.find(params[:id])
    end

    def update
        @volunteer = Volunteer.find(params[:id])
        if @volunteer.update(volunteer_params)
            redirect_to volunteer_path(@volunteer), notice: 'Volunteer was successfully updated.'
        else
            render :edit
        end
    end

    private

    def search_params
        params.permit(:program_name, :division_name, :team_name, :volunteer_role, 
        :volunteer_first_name, :volunteer_last_name, :volunteer_street_address, 
        :volunteer_address_unit, :volunteer_city, :volunteer_state, 
        :volunteer_postal_code, :volunteer_email_address, :volunteer_telephone, 
        :volunteer_cellphone, :volunteer_other_phone, :association_volunteer_id)
    end

    private

    def volunteer_params
        params.require(:volunteer).permit(:program_name, :division_name, :team_name, :volunteer_role, 
        :volunteer_first_name, :volunteer_last_name, :volunteer_street_address, 
        :volunteer_address_unit, :volunteer_city, :volunteer_state, 
        :volunteer_postal_code, :volunteer_email_address, :volunteer_telephone, 
        :volunteer_cellphone, :volunteer_other_phone, :association_volunteer_id)
    end
end
