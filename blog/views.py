from django.http import HttpResponse
from django.shortcuts import redirect, render
from blog.models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras

from django.http import HttpResponse
# Create your views here.
def blogHome(request):
    allPosts=Post.objects.all()
    context={'allPosts':allPosts}
    #return HttpResponse("Hello this is blogHome , we will keep all the blog posts here")
    return render(request,"blog/blogHome.html",context)

def blogPost(request,slug):
    try:
        post=Post.objects.filter(slug=slug).first()
        post.views+=1
        post.save()
        comments=BlogComment.objects.filter(post=post,parent=None)
        replies=BlogComment.objects.filter(post=post).exclude(parent=None)
        replyDict={}
        for reply in replies:
            if reply.parent.sno not in replyDict.keys():
                replyDict[reply.parent.sno]=[reply]
            else:
                replyDict[reply.parent.sno].append(reply)
        print(replyDict)
        context={'post':post,"comments":comments,"user":request.user,'replyDict':replyDict}
        return render(request,"blog/blogPost.html",context)
    except Exception as e:
        return HttpResponse("Error 404! Not found")

def postComment(request):
    if request.method=="POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno=request.POST.get("postSno")
        post=Post.objects.get(sno=postSno)
        parentSno=request.POST.get("parentSno")
        if parentSno=="":
            comment=BlogComment(comment=comment,user=user,post=post)
            comment.save()
            messages.success(request, "Your Comment has been posted successfully")
        else:
            parent=BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment=comment,user=user,post=post,parent=parent)
            comment.save()
            messages.success(request, "Your Reply has been posted successfully")
        
    return redirect(f"/blog/{post.slug}")
