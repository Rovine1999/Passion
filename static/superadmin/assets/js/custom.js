function limitText(text, limit) {
    if (text) {
        if (text.length > limit) {
            return text.substring(0, limit)
        }
        else {
            return text
        }
    }
    else {
        return "N/A"
    }
}

function specialityCard(speciality) {
    return `
        <span class="badge rounded bg-secondary mb-1">${speciality.name}</span>    
    `
}

function facilityImage(image, facility_name) {
    if (image) {
        return `
            <img src="${image}" loading="lazy" alt="" class="rounded">
        `
    }
    else {
        return `
        <div class="h-100 rounded bg-dark d-flex justify-content-center align-items-center p-2 text-center">
            <span class="widget-popular-product-title d-block text-white">
                ${facility_name}
            </span>
        </div>
        `
    }
}

function facilityCard(facility) {
    const specialities = facility?.specialities.map(speciality => specialityCard(speciality))

    return `
    <div class="card h-100 shadow border-0">
        <div class="card-body">
            <div class="widget-popular-product-container">
                <div class="facility-card-image">
                    ${facilityImage(facility?.image, facility?.name)}
                </div>
                <div class="hstack gap-2 py-2">
                    ${specialities}
                </div>
                <div class="widget-popular-product-content">
                    <a href="#"
                        class="widget-popular-product-title d-block" data-toggle="tooltip"
                        data-placement="top" title="{{facility.name}}">
                        <h4>
                            ${limitText(facility?.name, 25)}
                        </h4>
                    </a>
                    <p class="widget-popular-product-text">
                        ${limitText(facility?.description, 50)}
                    </p>
                    <div>
                        <p class="m-0 p-0">
                            <small>
                                County: ${facility?.county?.name}
                            </small>
                        </p>
                        <p class="m-0 p-0">
                            <small>
                                Constituency:
                                <span data-toggle="tooltip" data-placement="top"
                                    title="${facility?.constituency?.name}">
                                    ${limitText(facility?.constituency?.name, 20)}
                                </span>
                            </small>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `
}

function wrappedFacilityCard(facility) {
    return `
        <div class="col-md-4">
            ${facilityCard(facility)}
        </div>
    `
}

function getUserProfilePic(username, image) {
    if (image) {
        return `<img src="${image}" style="width: 95%" alt="">`
    }
    else {
        return `<div class="avatar-title">${limitText(username, 1)}</div>`
    }
}

function getUserActiveStatus(active, state_1, state_2) {
    if (active) {
        return `
            <div class="badge badge-success">${state_1}</div>
        `
    }
    return `<div class="badge badge-danger">${state_2}</div>    
        `
}

function basicUserInformation(user) {
    return `
    <div class="mb-3">
        <h2 class="mb-3">Basic User Information</h2>
        <div class="row">
            <div class="col-md-4">
                <div class="card shadow p-2 h-100 bg-light" style="">
                    <div class="d-flex justify-content-center flex-column">
                        <h4 class="text-center m-0 p-0">Profile Picture</h4>
                        <hr class="my-3">
                        <div class="avatar avatar-xxl mx-auto">
                            ${getUserProfilePic(user?.username, user?.profile?.profile_photo)}
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-8">
                <div class="card p-2 h-100">
                    <h4 class="m-0 p-0">Profile Details</h4>
                    <hr class="my-3">
                    <div class="v-stack">

                        <div class="row mb-2">
                            <div class="col-4">
                                <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">First Name: </h5>
                            </div>
                            <div class="col-8">
                                <p class="text-muted m-0 p-0">
                                    ${user?.first_name}
                                </p>
                            </div>
                        </div>

                        <div class="row mb-2">
                            <div class="col-4">
                                <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">Last Name: </h5>
                            </div>
                            <div class="col-8">
                                <p class="text-muted m-0 p-0">
                                   ${user?.last_name}
                                </p>
                            </div>
                        </div>

                        <div class="row mb-2">
                            <div class="col-4">
                                <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">Username: </h5>
                            </div>
                            <div class="col-8">
                                <p class="text-muted m-0 p-0">
                                    ${user?.username}
                                </p>
                            </div>
                        </div>

                        <div class="row mb-2">
                            <div class="col-4">
                                <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">Email: </h5>
                            </div>
                            <div class="col-8">
                                <p class="text-muted m-0 p-0">
                                    ${user?.email}
                                </p>
                            </div>
                        </div>

                        <div class="row mb-2">
                            <div class="col-4">
                                <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">Account Status:
                                </h5>
                            </div>
                            <div class="col-8">
                                ${getUserActiveStatus(user?.is_active, 'Active', 'In-Active')}
                            </div>
                        </div>
                        <div class="row mb-2">
                            <div class="col-4">
                                <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">Phone Number: </h5>
                            </div>
                            <div class="col-8">
                                <p class="text-muted m-0 p-0">
                                    ${user?.profile?.phone_number}
                                </p>
                            </div>
                        </div>

                    </div>

                </div>
            </div>
        </div>
    </div>
    `
}

function advancedUserInformation(user) {

    return `
    <div class="card p-2 h-100 my-5">
        <h4 class="m-0 p-0">Advanced User Details</h4>
        <hr class="my-3">
        <div class="v-stack">

            <div class="row mb-2">
                <div class="col-4">
                    <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">Date of Birth: </h5>
                </div>
                <div class="col-8">
                    <p class="text-muted m-0 p-0">
                        ${user?.profile?.dob}
                    </p>
                </div>
            </div>

            <div class="row mb-2">
                <div class="col-4">
                    <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">Age: </h5>
                </div>
                <div class="col-8">
                    <p class="text-muted m-0 p-0">
                        ${user?.profile?.dob}
                    </p>
                </div>
            </div>

            <div class="row mb-2">
                <div class="col-4">
                    <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">Gender: </h5>
                </div>
                <div class="col-8">
                    <p class="text-muted m-0 p-0 text-capitalize">
                        ${user?.profile?.gender}
                    </p>
                </div>
            </div>

            <div class="row mb-2">
                <div class="col-4">
                    <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">Address: </h5>
                </div>
                <div class="col-8">
                    <p class="text-muted m-0 p-0">
                        ${user?.profile?.address}
                    </p>
                </div>
            </div>

            <div class="row mb-2">
                <div class="col-4">
                    <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">Country: </h5>
                </div>
                <div class="col-8">
                    <p class="text-muted m-0 p-0 text-capitalize">
                        ${user?.profile?.country}
                    </p>
                </div>
            </div>
            <div class="row mb-2">
                <div class="col-4">
                    <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">City: </h5>
                </div>
                <div class="col-8">
                    <p class="text-muted m-0 p-0 text-capitalize">
                        ${user?.profile?.city}
                    </p>
                </div>
            </div>

        </div>

    </div>
    `
}

function qualificationRow(qualification) {
    return `
    <tr>
        <td>${qualification?.degree}</td>
        <td>${qualification?.university}</td>
        <td>${qualification?.year}</td>
    </tr>
    `
}

function minimalUserCard(user) {
    return `
        <div class="custom-name-holder" data-bs-toggle="modal" data-bs-target="#user-modal"
            data-bs-user="Username">
            <div class="avatar rounded-circle avatar-sm me-2 d-flex align-items-center justify-content-center bg-light text-capitalize p-1">
                ${getUserProfilePic(user?.profile?.profile_photo, user?.username)}
            </div>
            <div class="vstack gap-0">
                <p class="m-0 p-0">${user?.first_name} ${user?.last_name}</p>
                <p class="m-0 p-0">
                    <small>${user?.email}</small>
                </p>
            </div>
        </div>
    `
}

function minimalFacilityCard(facility) {
    return `
        <div class="custom-name-holder" data-bs-toggle="modal" data-bs-target="#user-modal"
            data-bs-user="Username">
            <div class="avatar rounded-circle avatar-sm me-2 d-flex align-items-center justify-content-center bg-light text-capitalize p-1">
                ${getUserProfilePic(facility?.name, facility?.logo)}
            </div>
            <div class="vstack gap-0">
                <p class="m-0 p-0">${facility?.name}</p>
                <p class="m-0 p-0">
                    <small>${facility?.email}</small>
                </p>
            </div>
        </div>
    `
}

function appointmentRow(appointment) {
    return `
    <tr>
        <td>${minimalUserCard(appointment?.patient?.user)}</td>
        <td>${minimalUserCard(appointment?.doctor?.user)}</td>
        <td>${minimalFacilityCard(appointment?.facility)}</td>
        <td>${appointment?.condition?.name}</td>
        <td>${appointment?.note}</td>
        <td>${getUserActiveStatus(appointment?.status, 'Completed', 'In Complete')}</td>
        <td>${appointment?.date}</td>
        <td>${appointment?.start_time}</td>
        <td>${appointment?.end_time}</td>
    </tr>
    `
}

function doctorDetails(doctor) {
    if(doctor){
    const facilities = doctor?.facilities?.map(facility => wrappedFacilityCard(facility))
    const appointments = doctor?.doctor_appointments?.map(appointment => appointmentRow(appointment))
    const qualifications = doctor?.qualifications?.map(qualification => qualificationRow(qualification))

    return `
        <div class="card p-2 h-100 my-5">
            <h4 class="m-0 p-0">Doctor Details</h4>
            <hr class="my-3">
            <div class="v-stack">

                <div class="row mb-2">
                    <div class="col-4">
                        <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">Status: </h5>
                    </div>
                    <div class="col-8">
                        ${getUserActiveStatus(doctor?.available, 'Available', 'Not-Available')}
                    </div>
                </div>

                <div class="row mb-2">
                    <div class="col-md-4">
                        <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">Description </h5>
                    </div>
                    <div class="col-md-8">
                        <p class="text-muted m-0 p-0">
                            ${doctor?.description}
                        </p>
                    </div>
                </div>

                <div class="row mb-2">
                    <div class="col-md-4">
                        <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">Registerd on: </h5>
                    </div>
                    <div class="col-md-8">
                        <p class="text-muted m-0 p-0">
                            ${doctor?.created_on}
                        </p>
                    </div>
                </div>

                <div class="facilities my-3">
                    <h4 class="m-0 p-0 py-3">Facilities</h4>
                    <div class="row">
                        ${facilities}
                    </div>
                </div>

                <div class="qualifications my-3">
                    <h4 class="m-0 p-0 py-3">Proffessional Qualifications</h4>
                    <div class="table-responsive">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Degree</th>
                                    <th>School/University</th>
                                    <th>Year</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${qualifications}
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="qualifications my-3">
                    <h4 class="m-0 p-0 py-3">Appointments</h4>
                    <div class="table-responsive">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th class="custom-th-text">Patient</th>
                                    <th class="custom-th-text">Doctor</th>
                                    <th class="custom-th-text">Facility</th>
                                    <th class="custom-th">Condition</th>
                                    <th class="custom-th-text">Note</th>
                                    <th class="custom-th">Status</th>
                                    <th class="custom-th">Date</th>
                                    <th class="custom-th">Start Time</th>
                                    <th class="custom-th">End Time</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${appointments}
                            </tbody>
                        </table>
                    </div>
                </div>

            </div>

        </div>
    `
    }
    return ""
}

function encounterRow(encounter) {
    return `
        <tr>
            <td>${minimalFacilityCard(encounter?.facility)}</td>
            <td>${minimalUserCard(encounter?.doctor)}</td>
            <td>${encounter?.notes}</td>
            <td>${encounter?.description}</td>
            <td>${encounter?.date}</td>
        </tr>
    `
}

function patientDetails(patient) {
    if(patient){
    const facilities = patient?.facilities?.map(facility => wrappedFacilityCard(facility))
    console.log(facilities)
    const appointments = patient?.patient_appointments?.map(appointment => appointmentRow(appointment))
    const encounters = patient?.patient_encounters?.map(encounter => encounterRow(encounter))

    return `
        <div class="card p-2 h-100 my-5">
            <h4 class="m-0 p-0">Patient Details</h4>
            <hr class="my-3">
            <div class="v-stack">

                <div class="row mb-2">
                    <div class="col-4">
                        <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">Blood Group: </h5>
                    </div>
                    <div class="col-8">
                        <p class="text-muted m-0 p-0">
                            ${patient?.blood_group}
                        </p>
                    </div>
                </div>

                <div class="row mb-2">
                    <div class="col-4">
                        <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">Account Sharable: </h5>
                    </div>
                    <div class="col-8">
                        ${getUserActiveStatus(patient?.account_sharable, 'Sharable', 'Not sharable')}
                    </div>
                </div>

                <div class="row mb-2">
                    <div class="col-md-4">
                        <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">Registerd on: </h5>
                    </div>
                    <div class="col-md-8">
                        <p class="text-muted m-0 p-0">
                            ${patient?.created_on}
                        </p>
                    </div>
                </div>

                <div class="facilities my-3">
                    <h4 class="m-0 p-0 py-3">Facilities</h4>
                    <div class="row">
                        ${facilities}
                    </div>
                </div>

                <div class="qualifications my-3">
                    <h4 class="m-0 p-0 py-3">Appointments</h4>
                    <div class="table-responsive">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th class="custom-th-text">Patient</th>
                                    <th class="custom-th-text">Doctor</th>
                                    <th class="custom-th-text">Facility</th>
                                    <th class="custom-th">Condition</th>
                                    <th class="custom-th-text">Note</th>
                                    <th class="custom-th">Status</th>
                                    <th class="custom-th">Date</th>
                                    <th class="custom-th">Start Time</th>
                                    <th class="custom-th">End Time</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${appointments}
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="qualifications my-3">
                    <h4 class="m-0 p-0 py-3">Patient Medical Information</h4>
                    <div class="table-responsive">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th class="custom-th">Facility</th>
                                    <th class="custom-th">Doctor</th>
                                    <th class="custom-th-text">Notes</th>
                                    <th class="custom-th">description</th>
                                    <th class="custom-th">Date</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${encounters}
                            </tbody>
                        </table>
                    </div>
                </div>

            </div>

        </div>
    `
    }
    return ""
}

function staffDetails(staff) {
    if (staff) {
        const facility = staff?.facility ? facilityCard(staff?.facility) : ""
        return `
        <div class="card p-2 h-100 my-5">
            <h4 class="m-0 p-0">Staff Details</h4>
            <hr class="my-3">
            <div class="v-stack">

                <div class="row mb-2">
                    <div class="col-4">
                        <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">Designation: </h5>
                    </div>
                    <div class="col-8">
                        <p class="text-muted m-0 p-0">
                            ${staff?.designation}
                        </p>
                    </div>
                </div>

                <div class="row mb-2">
                    <div class="col-4">
                        <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">Education: </h5>
                    </div>
                    <div class="col-8">
                        <div class="badge">
                            ${staff?.education}
                        </div>
                    </div>
                </div>

                <div class="row mb-2">
                    <div class="col-md-4">
                        <h5 class="fs-c m-0 p-0 me-2" style="font-weight: 500;">Registered on: </h5>
                    </div>
                    <div class="col-md-8">
                        <p class="text-muted m-0 p-0">
                            ${staff?.created_on}
                        </p>
                    </div>
                </div>

                <div class="facilities my-3">
                    <h4 class="m-0 p-0 py-3">Facilities</h4>
                    <div class="row">
                        <div class="col-md-4">
                            ${facility}
                        </div>
                    </div>
                </div>

            </div>

        </div>
    `
    }
    return ""
}
