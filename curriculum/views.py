from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django import forms

from mentortogether.curriculum.models import Curriculum
from mentortogether.curriculum.models import CurriculumNode

@permission_required('Curriculum.change_curriculum')
def add_section(request, cid):

    curriculum = get_object_or_404(Curriculum, pk=cid)
    form = None
    errors = False

    class SectionForm(forms.ModelForm):
        title = forms.CharField(required=True)
        class Meta:
            model  = CurriculumNode
            fields = ('title', 'rank', 'summary')

    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.curriculum = curriculum
            section.mentor_doc = ''
            section.mentee_doc = ''
            section.section = None
            section.create_by = request.user
            section.edit_by = request.user
            section.is_section = True
            section.is_active = True
            section.save()
            return redirect("view-curriculum", cid=curriculum.id)
    else:
        form = SectionForm()

    return render_to_response('curriculum/add_section.html', 
                              { 'form'       : form,
                                'curriculum' : curriculum },
                              context_instance=RequestContext(request))


@permission_required('Curriculum.change_curriculum')
def edit_section(request, cid, sid):
    """
    Edit/Save curriculum section node.
    """
    section = get_object_or_404(CurriculumNode, pk=sid)
    form    = None
    errors  = False

    class EditForm(forms.ModelForm):
        title = forms.CharField(required=True)
        class Meta:
            model  = CurriculumNode
            fields = ('title', 
                      'rank', 
                      'summary',
                      'is_active')

    if request.method == 'POST':
        form = EditForm(request.POST, instance=section)
        if form.is_valid():
            section = form.save(commit=False)
            section.create_by = request.user
            section.edit_by = request.user
            section.save()
            return redirect("view-section", cid=section.curriculum.id,
                                            sid=section.id)
    else:
        form = EditForm(instance=section)

    return render_to_response('curriculum/edit_section.html', 
                              { 'form'       : form,
                                'section'    : section,
                                'curriculum' : section.curriculum },
                              context_instance=RequestContext(request))


    
@permission_required('Curriculum.change_curriculum')
def add_curriculum(request):

    class AddForm(forms.ModelForm):
        title = forms.CharField(label='Title', required=True)
        class Meta:
            model  = Curriculum
            fields = ('title', 'summary')

    form   = None
    errors = False

    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            cclm = form.save(commit=False)
            cclm.is_active = True
            cclm.save()
            return redirect("index")
        else:
            error = True
    else:
        form = AddForm()
    return render_to_response('curriculum/add_curriculum.html', 
                              { 'form'  : form },
                              context_instance=RequestContext(request))

@permission_required('Curriculum.change_curriculum')
def edit_curriculum(request, cid):

    curriculum = get_object_or_404(Curriculum, pk=cid)

    class EditForm(forms.ModelForm):
        title = forms.CharField(label='Title', required=True)
        class Meta:
            model  = Curriculum
            fields = ('title', 'summary')

    form   = None
    errors = False

    if request.method == 'POST':
        form = EditForm(request.POST, instance=curriculum)
        if form.is_valid():
            cclm = form.save(commit=False)
            cclm.is_active = True
            cclm.save()
            return redirect("view-curriculum", cid=curriculum.id)
        else:
            error = True
    else:
        form = EditForm(instance=curriculum)
    return render_to_response('curriculum/edit_curriculum.html', 
                              { 'form'       : form,
                                'curriculum' : curriculum },
                              context_instance=RequestContext(request))



@permission_required('Curriculum.change_curriculum')
def edit_prompt(request, cid, sid, pid):
    """
    Edit/Save a writing prompt.
    """
    form = None

    class EditForm(forms.ModelForm):
        title = forms.CharField(required=True)
        class Meta:
            model  = CurriculumNode
            fields = ('title',
                      'rank',
                      'summary',
                      'mentor_doc',
                      'mentee_doc',
                      'is_active')

    prompt = get_object_or_404(CurriculumNode, pk=pid)

    if request.method == 'POST':
        form = EditForm(request.POST, instance=prompt)
        if form.is_valid():
            prompt = form.save(commit=False)
            prompt.edit_by = request.user
            prompt.save()
            return redirect("view-section", cid=prompt.section.curriculum.id,
                                            sid=prompt.section.id)
    else:
        form = EditForm(instance=prompt)
 
    return render_to_response('curriculum/edit_prompt.html', 
                              { 'form'       : form,
                                'prompt'     : prompt,
                                'section'    : prompt.section,
                                'curriculum' : prompt.section.curriculum },
                              context_instance=RequestContext(request))

@permission_required('Curriculum.change_curriculum')
def add_prompt(request, cid, sid):

    section = get_object_or_404(CurriculumNode, pk=sid)

    class PromptForm(forms.ModelForm):
        title = forms.CharField(required=True)
        class Meta:
            model  = CurriculumNode
            fields = ('title',
                      'rank',
                      'summary',
                      'mentor_doc',
                      'mentee_doc')
 
    if request.method == 'POST':
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = form.save(commit=False)
            prompt.curriculum = section.curriculum
            prompt.section = section
            prompt.create_by = request.user
            prompt.edit_by = request.user
            prompt.is_section = False
            prompt.is_active = True
            prompt.save()
            return redirect("view-section", cid=section.curriculum.id,
                                            sid=section.id)
    else:
        form = PromptForm()

    return render_to_response('curriculum/add_prompt.html', 
                              { 'form'       : form,
                                'curriculum' : section.curriculum,
                                'section'    : section },
                              context_instance=RequestContext(request))

    
@permission_required('Curriculum.change_curriculum')
def view_section(request, cid, sid):
    section = get_object_or_404(CurriculumNode, pk=sid)
    prompts = CurriculumNode.objects.filter(section=section,
                                            is_section=False).order_by('rank')
    return render_to_response('curriculum/view_section.html',
                               { 'curriculum' : section.curriculum,
                                 'section'    : section,
                                 'prompts'    : prompts },
                              context_instance=RequestContext(request))


@permission_required('Curriculum.change_curriculum')
def view_curriculum(request, cid):
    curriculum = get_object_or_404(Curriculum, pk=cid)
    sections   = CurriculumNode.objects.filter(curriculum=curriculum, 
                                               is_section=True).order_by('rank')
    return render_to_response('curriculum/view_curriculum.html',
                              { 'curriculum' : curriculum,
                                'sections'   : sections },
                              context_instance=RequestContext(request))

@permission_required('Curriculum.change_curriculum')
def main(request):
    """
    Main curriculum prompt.
    """
    curriculums = Curriculum.objects.all()
    return render_to_response('curriculum/main.html',
                              { 'curriculums' : list(curriculums) },
                              context_instance=RequestContext(request))
